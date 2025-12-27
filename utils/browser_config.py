"""
Browser configuration module.
Determines which browsers to use based on the execution environment.
- Jenkins: Only Chrome
- GitHub Actions or Local PC: Both Chrome and Edge
"""
import os


def get_browsers():
    """
    Returns a list of browsers to test with based on the environment.

    Returns:
        list: List of browser names ('chrome', 'edge')
    """
    # Check if running in Jenkins
    # Jenkins sets JENKINS_HOME or BUILD_NUMBER environment variables
    is_jenkins = os.environ.get('JENKINS_HOME') or os.environ.get('BUILD_NUMBER')

    if is_jenkins:
        # Jenkins: Use only Chrome
        return ["chrome"]
    else:
        # GitHub Actions or Local PC: Use both Chrome and Edge
        return ["chrome", "edge"]

