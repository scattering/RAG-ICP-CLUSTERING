# NOTE: I could not get this working using the OpenAI API.
require 'net/http'
require 'uri'
require 'json'
require 'logger'

# Set up logging
logger = Logger.new(STDOUT)
logger.level = Logger::INFO  # Change to Logger::DEBUG for more detailed logging

# Constants
MAVERICK = "Llama-4-Maverick-17B-128E-Instruct-FP8"
ENDPOINT_BASE = "https://rchat.nist.gov/api"
CHAT_ENDPOINT = "#{ENDPOINT_BASE}/chat/completions"
API_KEY = ENV['RCHAT_API_KEY'] || raise("Missing RCHAT_API_KEY environment variable")

# Function to directly call the Llama API
def ask_llama(question, logger, model = MAVERICK)
  uri = URI.parse(CHAT_ENDPOINT)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  http.verify_mode = OpenSSL::SSL::VERIFY_NONE  # Skip SSL verification
  http.open_timeout = 240
  http.read_timeout = 240
  
  # Create request
  request = Net::HTTP::Post.new(uri.path)
  
  # Set headers
  request["Content-Type"] = "application/json"
  request["Authorization"] = "Bearer #{API_KEY}"
  request["Accept"] = "application/json"
  
  # Set request body
  payload = {
    messages: [
      { role: "user", content: question }
    ],
    model: model,
    max_tokens: 128,
    temperature: 0.7,
    top_p: 0.95,
    stream: false
  }
  
  logger.debug("Sending request to: #{CHAT_ENDPOINT}")
  
  # Set the request body
  request.body = payload.to_json
  
  begin
    # Send the request
    logger.debug("Sending request...")
    response = http.request(request)
    
    if response.code.to_i == 200
      result = JSON.parse(response.body)
      return result.dig("choices", 0, "message", "content")
    else
      logger.error("Error Response: #{response.code} - #{response.body}")
      return nil
    end
  rescue => e
    logger.error("Request Error: #{e.message}")
    return nil
  end
end

# Main program
puts "Enter your question (or 'exit' to quit):"
while (question = gets.chomp) != "exit"
  puts "\nSending your question..."
  response = ask_llama(question, logger)
  
  if response
    puts "\nResponse:"
    puts "#{response}"
  else
    puts "\nNo response received or error occurred. Check logs for details."
  end
  
  puts "\nEnter your question (or 'exit' to quit):"
end

puts "Goodbye!"
