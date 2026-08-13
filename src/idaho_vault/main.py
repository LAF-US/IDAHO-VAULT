import sys
import os
from idaho_vault.crew import FiveWizardsCouncil

def run():
    """
    Run the 5Wizards Council Crew.
    """
    inputs = {
        'topic': 'The current state of the manus/self-testing dimension'
    }
    FiveWizardsCouncil().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
