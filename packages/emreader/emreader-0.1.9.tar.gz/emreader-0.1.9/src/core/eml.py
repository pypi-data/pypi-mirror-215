import glob
import os
import email
from email import policy
from multiprocessing import Pool
import rich

EXTENSION = "eml"

current_dir = os.path.dirname(os.path.abspath(__file__))
storage_dir = os.path.join(current_dir, "..", "storage", "source", "emails")
output_dir = os.path.join(current_dir, "..", "storage", "output")


def extract(filename):
    """
    Try to extract the attachments from all files in cwd
    """
    os.makedirs(output_dir, exist_ok=True)
    output_count = 0
    try:
        with open(filename, "r") as f:
            msg = email.message_from_file(f, policy=policy.default)
            for idx, attachment in enumerate(msg.iter_attachments()):
                try:
                    # Only proceed if the attachment is a PDF
                    if attachment.get_filename().lower().endswith(".pdf"):
                        # Generate a short uuid
                        subject = msg['subject']
                        subject = subject.replace(" ", "_").lower()
                        output_filename = f"{subject}.pdf"
                    else:
                        continue
                except AttributeError:
                    print(f"Got string instead of filename for {f.name}. Skipping.")
                    continue
                
                if output_filename:
                    with open(os.path.join(output_dir, output_filename), "wb") as of:
                        try:
                            of.write(attachment.get_payload(decode=True))
                            output_count += 1
                        except TypeError:
                            print(f"Couldn't get payload for {output_filename}")
            if output_count == 0:
                print(f"No attachment found for file {f.name}!")
    except IOError:
        print(f"Problem with {f.name} or one of its attachments!")
    
    return 1, output_count


def extract_from_file(f):
    
    msg = email.message_from_binary_file(f, policy=policy.default)
    for idx, attachment in enumerate(msg.iter_attachments()):
        try:
            # Only proceed if the attachment is a PDF
            if attachment.get_filename().lower().endswith(".pdf"):
                # Generate a short uuid
                subject = msg['subject']
                subject = subject.replace(" ", "_").lower()
                output_filename = f"{subject}.pdf"
            else:
                continue
        except AttributeError:
            print(f"Got string instead of filename for {f.name}. Skipping.")
            continue
        
        if output_filename:
            with open(os.path.join(output_dir, output_filename), "wb") as of:
                try:
                    of.write(attachment.get_payload(decode=True))
                except TypeError:
                    print(f"Couldn't get payload for {output_filename}")
    
    return "Done"



def extract_emails():
    rich.print(f"in {storage_dir}, extracting emails")
    pool = Pool(None)
    eml_files = glob.glob(os.path.join(storage_dir, f"*.{EXTENSION}"))
    res = pool.map(extract, eml_files)
    pool.close()
    pool.join()
    
    numfiles = [sum(i) for i in zip(*res)]
    rich.print(f"Done: Processed {numfiles}.")
