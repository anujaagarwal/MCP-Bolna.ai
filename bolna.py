import httpx
from mcp.server.fastmcp import FastMCP
from typing import Any

# Initialize the MCP server
mcp = FastMCP("BolnaVoiceAI")

# Bolna API base URL and authentication header
BOLNA_API_URL = "https://api.bolna.ai/v2"
API_KEY = "bn-e9c06115e04144bebd6d5aa7c20b5716"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Asynchronous function to make requests to the Bolna API
async def make_bolna_request(url: str, method: str = "GET", data: dict = None) -> dict[str, Any] | None:
    """Make a request to the Bolna API with error handling."""
    async with httpx.AsyncClient() as client:
        try:
            if method == "POST":
                response = await client.post(url, json=data, headers=HEADERS, timeout=30.0)
            elif method == "PUT":
                response = await client.put(url, json=data, headers=HEADERS, timeout=30.0)
            elif method == "DELETE":
                response = await client.delete(url, headers=HEADERS, timeout=30.0)
            else:  # GET method
                response = await client.get(url, headers=HEADERS, timeout=30.0)

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

# Tool to create a new agent
@mcp.tool()
async def create_agent(agent_config: dict) -> dict:
    """Create a new voice AI agent."""
    url = f"{BOLNA_API_URL}/agent"
    return await make_bolna_request(url, "POST", agent_config)

# Tool to retrieve all agents
@mcp.tool()
async def get_agents() -> list:
    """Retrieve all voice AI agents."""
    url = f"{BOLNA_API_URL}/agent/all"
    return await make_bolna_request(url)

# Tool to retrieve a specific agent by ID
@mcp.tool()
async def get_agent(agent_id: str) -> dict:
    """Retrieve a specific voice AI agent by ID."""
    url = f"{BOLNA_API_URL}/agent/{agent_id}"
    return await make_bolna_request(url)

# Tool to update an agent
@mcp.tool()
async def update_agent(agent_id: str, agent_config: dict) -> dict:
    """Update an existing voice AI agent."""
    url = f"{BOLNA_API_URL}/agent/{agent_id}"
    return await make_bolna_request(url, "PUT", agent_config)

# Tool to delete an agent
@mcp.tool()
async def delete_agent(agent_id: str) -> dict:
    """Delete a voice AI agent."""
    url = f"{BOLNA_API_URL}/agent/{agent_id}"
    response = await make_bolna_request(url, "DELETE")
    return {"status": "deleted"} if response is None else response

# Tool to execute an agent
@mcp.tool()
async def execute_agent(agent_id: str, execution_data: dict) -> dict:
    """Execute a voice AI agent."""
    url = f"{BOLNA_API_URL}/executions/{agent_id}"
    return await make_bolna_request(url, "POST", execution_data)

# Tool to retrieve execution status
@mcp.tool()
async def get_execution_status(execution_id: str) -> dict:
    """Retrieve the status of a specific execution."""
    url = f"{BOLNA_API_URL}/executions/status/{execution_id}"
    return await make_bolna_request(url)

# Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
