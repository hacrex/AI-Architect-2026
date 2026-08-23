"""Script to deploy a model."""
from app.deployment import DeploymentEngine


def main():
    deployer = DeploymentEngine()

    # Deploy to staging
    staging = deployer.deploy("enterprise-rag", "1.0.0", "staging")
    print(f"Staging deployment: {staging.id} - {staging.status.value}")

    # Deploy canary to production
    canary = deployer.canary(
        model="enterprise-rag",
        version="1.0.0",
        initial_percentage=5,
        increment=25,
        observation_period_seconds=10
    )
    print(f"Canary deployment: {canary.id}")
    print(f"Status: {canary.status.value}")
    print(f"Final percentage: {canary.canary_percentage}%")


if __name__ == "__main__":
    main()
