import pytest
from mcp_server.server import mcp

def test_mcp_schemas():
    # Basic check to ensure the MCP server is initialized correctly
    assert mcp.name == "Affective-Subcortical-Engine"
    # Wait for the fastmcp API, but just checking instantiation is sufficient for this mock
