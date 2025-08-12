  <h1>RAG-ICP-CLUSTERING</h1>
  <h2>Applications of Large Language Models and AI to Neutron Scattering</h2>
  <p><strong>Author:</strong> Aditya Purohit (Richard Montgomery High School)</p>
  <p><strong>Mentor:</strong> Dr. William Ratcliff, NIST Center for Neutron Research (NCNR)</p>

  <h2>Overview</h2>
  <p>This project integrates Large Language Models (LLMs) and AI-powered tools into neutron scattering research workflows at the NIST Center for Neutron Research.</p>
  <p>The NCNR serves a diverse user base, many of whom are not deeply familiar with specific instruments or related prior work.</p>
  <p>Our system uses the Model Context Protocol (MCP) to connect LLMs with validated NCNR tools and datasets, improving research efficiency and accessibility.</p>

  <h2>Key Components</h2>

  <h3>1. Instrument Control Program (ICP) Tool</h3>
  <ul>
    <li>Computes motor angles for triple-axis spectrometers based on crystallographic inputs.</li>
    <li>Allows natural language descriptions of experimental setups via a chat interface.</li>
    <li><strong>Benefits:</strong>
      <ul>
        <li>Reduces setup complexity.</li>
        <li>Speeds up configuration.</li>
        <li>Makes instrumentation more accessible to non-expert users.</li>
      </ul>
    </li>
  </ul>

  <h3>2. BT7 Retrieval-Augmented Generation (RAG) Tool</h3>
  <ul>
    <li>Uses a database of NCNR publications (2016–2017) to answer natural language queries.</li>
    <li>Links queries to prior BT7 experiments, showing setups, parameters, and results.</li>
    <li><strong>Benefits:</strong>
      <ul>
        <li>Speeds up literature searches.</li>
        <li>Improves accuracy of experiment planning.</li>
      </ul>
    </li>
  </ul>

  <h3>3. Proposal Classifier &amp; Clustering Tool</h3>
  <ul>
    <li>Applies semantic search and RAG-based clustering to incoming NCNR proposals.</li>
    <li>Groups proposals by scientific theme to streamline review.</li>
    <li><strong>Benefits:</strong>
      <ul>
        <li>Highlights thematic overlaps.</li>
        <li>Creates clusters with descriptive keywords.</li>
      </ul>
    </li>
  </ul>

  <h2>Methodology</h2>
  <ul>
    <li><strong>Data Integration:</strong> NCNR publications and proposal documents ingested into searchable formats.</li>
    <li><strong>MCP Interface:</strong> LLMs connected to specialized tools through a secure API.</li>
    <li><strong>Tool Development:</strong> ICP Tool for instrument setup; RAG Tool for targeted literature retrieval; Clustering tool for thematic grouping of proposals.</li>
  </ul>

  <h2>Results</h2>
  <ul>
    <li>Faster literature searches for experiment planning.</li>
    <li>Reduced setup complexity in instrument configurations.</li>
    <li>Streamlined proposal review through thematic clustering.</li>
    <li>Increased accessibility of advanced NCNR tools to non-experts.</li>
  </ul>

  <h2>Future Directions</h2>
  <ul>
    <li>Expand RAG database to include all NCNR instruments and external labs.</li>
    <li>Integrate clustering outputs with reviewer assignment systems.</li>
    <li>Create seamless, multi-tool workflows connecting setup, search, and review.</li>
  </ul>

  <h2>Acknowledgements</h2>
  <ul>
    <li>Mentor: Dr. William Ratcliff</li>
    <li>Infrastructure &amp; Review: Dr. Paul Kienzle</li>
    <li>Administrative Support: Dr. Julie Borchers</li>
    <li>Program Support: NIST SHIP Program</li>
    <li>Personal Support: Parents and all who contributed.</li>
  </ul>

<h2>Getting Started</h2>
<pre><code>git clone https://github.com/scattering/RAG-ICP-CLUSTERING.git
cd RAG-ICP-CLUSTERING

# Create and activate a conda environment
conda create --name rag-env python=3.12-y
conda activate rag-env

# Install required packages
pip install -r requirements.txt
</code></pre>
<p>Use the provided scripts to run the ICP, RAG, or clustering tools. Documentation and examples will be added for each module.</p>

<p>Create a <code>.env</code> file in the project root directory and add your RChat API key like this:</p>
<pre><code>RCHAT_API_KEY=your_rchat_api_key_here
</code></pre>
<p>Replace <code>your_rchat_api_key_here</code> with your actual RChat API key.</p>
<pre><code>
  
# Configure the MCP server

The file `config.json` contains a list of MCP servers that will be made available for your local Open WevUI instance:
- `count.py`: python tool that counts the number of times a letter appears in a word
- `calculator.py`: python tool that provides basic mathematical and statistical operations

# Start the MCP server

From the `mcp_server` folder, with your python env activated, run the following command:
```shell
uvx mcpo --port 8081 --api-key "CHANGE_ME" --config ./config.json
```
</code></pre>
**Notes:** 
- api-key should be a random string, this is **NOT your Rchat API KEY**,
- an api-key is provided in the `mcpo` documentation as an example and should be changed.

<h3>Start Python Embedding</h3>
<p>Run the following command to start the Python embedding in RAG_ICP_CLUSTERING:</p>
<pre><code>python BAAI_LARGE.py
</code></pre>

<h3>Start Open Web UI</h3>
<p>Navigate to the <code>nist-chat-main/rag_execution</code> directory and run the frontend with:</p>
<pre><code>cd RAG-ICP-CLUSTERING/nist-chat-main/rag_execution
python launch_frontend.py
</code></pre>

## Register the tools in your local Open WebUI

In a browser, go to your local Open WebUI instance, and add the tools in the admin dashboard.

Each MCP server from the `config.json` file needs to be added (2 in this case):
<pre><code>
- Count
  - URL: http://localhost:8081/database
  - API KEY: the api-key set in the mcpo command
  - Name: CreateDB
- Calculator:
  - URL: http://localhost:8081/LatticeCalculator
  - API KEY: the api-key set in the mcpo command
  - Name: Lattice Calculator
</code></pre>
...And so forth

Then you should be ready to use the tools in the Open-Webui interface, and prompting them to activate.
