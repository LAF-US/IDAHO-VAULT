from idaho_vault.crew import FiveWizardsCouncil
from idaho_vault.runtime import configure_vault_runtime


def run(topic: str = "The current state of the manus/self-testing dimension") -> None:
    """Run one bounded 5Wizards Council inquiry in vault-local runtime paths."""
    configure_vault_runtime()
    FiveWizardsCouncil().crew().kickoff(inputs={"topic": topic})


if __name__ == "__main__":
    run()
