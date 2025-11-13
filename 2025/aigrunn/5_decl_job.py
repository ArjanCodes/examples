from pydantic import BaseModel

from declarative_engine import run_declarative_flow


class ApplicantInfo(BaseModel):
    full_name: str
    years_experience: int
    has_degree: bool
    willing_to_relocate: bool


def main():
    instructions = """
        You are an Gronings dialect speaking HR assistant helping screen job applicants.
        Collect the required information speaking Gronings dialect only.
        """

    result = run_declarative_flow(
        model_type=ApplicantInfo,
        domain_instructions=instructions,
        debug=True,  # Disable for production
    )

    print("\n=== Final Applicant Info ===")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
