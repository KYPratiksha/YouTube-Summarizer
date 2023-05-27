#Importing necessary libraries
import tkinter as tk
import youtube_transcript_api
import webbrowser

# Initialize the Tkinter window
window = tk.Tk()
window.geometry("750x600")
window.title("YouTube Transcript Viewer")

# Define a label to prompt the user for input
label = tk.Label(window, text="Enter a YouTube URL:")
label.pack()

# Define a text entry field for the user to input the URL
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Define a function to retrieve the transcript and display it in a new window
def show_transcript():
    global transcript
    global url

    url = url_entry.get()

    # Retrieve the transcript for the video using the youtube_transcript_api module
    try:
        transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id=url.split("=")[-1])
        transcript = "\n".join([t['text'] for t in transcript_list])

        # Call the convert_to_pdf function to convert and download the transcript as a PDF
        convert_to_pdf(transcript)

        summary(transcript)
        print(summary)


    except youtube_transcript_api._errors.TranscriptNotFoundError:
        transcript = "Transcript not available for this video"

#Converting transcript to a pdf
def convert_to_pdf(transcript):

    from fpdf import FPDF

    # Create a new PDF object
    pdf = FPDF()

    # Add a new page to the PDF
    pdf.add_page()

    # Set the font and font size for the text
    pdf.set_font("Arial", size=12)

    # Add some text to the page
    result = transcript.split("\n")
    c = 2000
    for line in result:
        # print(line)
        pdf.cell(c, 10, line, ln=1)
        c += 5

    # Save the PDF file
    pdf.output("output.pdf")
    webbrowser.open("output.pdf")

#generating summary
def summary(transcript):
    from summa import summarizer

    # Set the desired ratio of the summary (e.g., 0.1 for 10% summary)
    summary_ratio = 0.3

    # Generate the summary using the TextRank algorithm
    summary = summarizer.summarize(transcript, ratio=summary_ratio)

    # Print the summary
    # print(summary)
    text_box.insert(tk.END, summary)

#text box widget
text_box = tk.Text(window)
text_box.pack()

# Add a button to submit the URL input
submit_button = tk.Button(window, text="Trancript", command=show_transcript)
submit_button.pack()

submit_button = tk.Button(window, text="Summary", command=lambda:summary)
submit_button.pack()

window.mainloop()

