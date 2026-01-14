from .evaluator import EvaluatorTestCase, main
from .agent import simple_agent
from langchain.messages import HumanMessage, ToolMessage

class POCEvaluator(EvaluatorTestCase):
    
    def __init__(self):
        super().__init__(name="poc_evaluator")

    def _invoke_agent(self, query: str) -> dict:
        """Helper method to invoke the agent with a query."""
        messages = [HumanMessage(content=query)]
        return simple_agent.invoke({"messages": messages})

    def _count_tool_calls(self, response: dict) -> int:
        """Count the number of tool calls made by the agent."""
        tool_calls = 0
        for message in response["messages"]:
            if isinstance(message, ToolMessage):
                tool_calls += 1
        return tool_calls

    def test_get_user_repositories(self):
        """Test that the agent can correctly fetch and return user repositories."""
        response = self._invoke_agent("List the repositories for user 'octocat'")
        
        final_response = response["messages"][-1].content.lower()
        
        # Check that the response mentions repositories or repos
        assert "repo" in final_response or "repository" in final_response or "spoon-knife" in final_response, \
            f"Agent did not return repository information. Response: {final_response[:200]}"

    def test_get_releases(self):
        """Test that the agent can correctly fetch and return releases for a repository."""
        response = self._invoke_agent("Get the releases for the repository 'facebook/react'")
        
        final_response = response["messages"][-1].content.lower()
        
        # Check that the response contains release-related information
        assert "release" in final_response or "version" in final_response or "v" in final_response, \
            f"Agent did not return release information. Response: {final_response[:200]}"

    def test_tool_call_efficiency_repositories(self):
        """Test that the agent doesn't use too many tool calls to fetch repositories."""
        response = self._invoke_agent("What repositories does the user 'torvalds' have?")
        
        tool_calls = self._count_tool_calls(response)
        max_expected_calls = 3  # Should only need 1-2 calls: get_user_repos (and maybe get_current_user)
        
        assert tool_calls <= max_expected_calls, \
            f"Agent used too many tool calls ({tool_calls}) to fetch repositories. Expected <= {max_expected_calls}"

    def test_tool_call_efficiency_releases(self):
        """Test that the agent doesn't use too many tool calls to fetch releases."""
        response = self._invoke_agent("Show me the releases for 'microsoft/vscode'")
        
        tool_calls = self._count_tool_calls(response)
        max_expected_calls = 3  # Should only need 1-2 calls: get_releases
        
        assert tool_calls <= max_expected_calls, \
            f"Agent used too many tool calls ({tool_calls}) to fetch releases. Expected <= {max_expected_calls}"

    def test_combined_query_efficiency(self):
        """Test that the agent handles combined queries efficiently."""
        response = self._invoke_agent("Get the releases and contributors for 'langchain-ai/langchain'")
        
        tool_calls = self._count_tool_calls(response)
        max_expected_calls = 5  # Should need around 2-3 calls: get_releases + get_repo_contributors
        
        assert tool_calls <= max_expected_calls, \
            f"Agent used too many tool calls ({tool_calls}) for combined query. Expected <= {max_expected_calls}"

        
if __name__ == "__main__":
    main()