from fastmcp import FastMCP
import subprocess
import os
import sys
import psutil  # make sure you install: pip install psutil
import subprocess
DETACHED_PROCESS = 0x00000008
mcp = FastMCP(name="ManageEmbeddingServer")

# We'll keep track of the PID in a file
PID_FILE = ""

@mcp.tool()
async def start_embedding_server(host: str = "0.0.0.0", port: int = 8888) -> str:
    """
    Starts the embedding.py FastAPI server as a subprocess.
    """
    if os.path.exists(PID_FILE):
        return "⚠️ Server appears to be already running (pid file exists). Check status or stop first."

    try:
        script_path = os.path.abspath("embedding.py")
        cmd = [sys.executable, script_path]
        process = subprocess.Popen(
        cmd,
        creationflags=DETACHED_PROCESS,
        close_fds=True
            )

        # Save the PID
        with open(PID_FILE, "w") as f:
            f.write(str(process.pid))

        return f"✅ embedding.py server started with PID {process.pid} on http://{host}:{port}"
    except Exception as e:
        return f"❌ Failed to start embedding.py: {str(e)}"

@mcp.tool()
async def stop_embedding_server() -> str:
    """
    Stops the embedding.py FastAPI server if it's running.
    """
    if not os.path.exists(PID_FILE):
        return "⚠️ No PID file found. Server may not be running."

    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read())

        # Use psutil to safely terminate
        p = psutil.Process(pid)
        p.terminate()
        p.wait(timeout=5)

        os.remove(PID_FILE)
        return f"🛑 Server with PID {pid} stopped successfully."
    except Exception as e:
        return f"❌ Failed to stop server: {str(e)}"

@mcp.tool()
async def status_embedding_server() -> str:
    """
    Checks if the embedding.py server is running.
    """
    if not os.path.exists(PID_FILE):
        return "📊 Server is not running (no PID file)."

    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read())

        if psutil.pid_exists(pid):
            p = psutil.Process(pid)
            return f"✅ Server is running with PID {pid}. Status: {p.status()}."
        else:
            return f"⚠️ Server PID {pid} not found. It may have stopped unexpectedly."
    except Exception as e:
        return f"❌ Could not check status: {str(e)}"

if __name__ == "__main__":
    mcp.run()
