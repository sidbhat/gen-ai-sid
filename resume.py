import streamlit as st


def main():
    # Request for a resume file in PDF
    resume_file = input("Please enter the path to your resume file in PDF: ")

    # Upload the resume
    resume = st.file_uploader(resume_file)

    # Highlight the skills section in blue
    skills = resume.get_skills()
    for skill in skills:
        resume.highlight_text(skill, color="blue")

    # Highlight the experience section in green
    experience = resume.get_experience()
    for experience in experience:
        resume.highlight_text(experience["title"], color="green")
        resume.highlight_text(experience["company"], color="green")

    # Highlight the LinkedIn profile in red
    linkedin_profile = resume.get_linkedin_profile()
    resume.highlight_text(linkedin_profile["url"], color="red")

    # Highlight the learning section in yellow
    learning = resume.get_learning()
    for learning in learning:
        resume.highlight_text(learning["title"], color="yellow")
        resume.highlight_text(learning["institution"], color="yellow")

    # Save the highlighted resume
    scallop.save_resume("my_highlighted_resume.pdf", resume)

if __name__ == "__main__":
    main()
