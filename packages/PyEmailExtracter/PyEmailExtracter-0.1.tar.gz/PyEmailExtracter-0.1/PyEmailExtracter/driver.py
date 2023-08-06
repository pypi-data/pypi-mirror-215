from helper import *


# Example: "/home/user_name/some_directory/resumes"
directory = str(input("Paste the absolute path of the directory and press enter.\n"))
file_extensions = [".docx", ".pdf"]
files = fetch_files(directory, file_extensions)

with open("total_files.txt", "a") as f:
    f.write("Total files fetched: \n" + str(len(files)) + "\n")


for file in files:
    current_ext = str(file).split(".")[1]
    if current_ext == "pdf":
        emails = extract_email_from_pdf(file)
    elif current_ext == "docx":
        emails = extract_email_from_docx(file)
    else:
        print("Currently we dont support ", str(current_ext))
    for email in emails:
        with open("email_list.txt", "a") as f:
            f.write(str(email) + "\n")
