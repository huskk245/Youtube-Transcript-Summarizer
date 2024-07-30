from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import nltk
nltk.download('punkt')
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

app = Flask(__name__)

# Define your routes and functions here


@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    summary_text = ""  # Provide a default value
    if request.method == 'POST':
        video_link = request.form.get('video_link')
        parsed_url = urlparse(video_link)
        query = parse_qs(parsed_url.query)
        vid_id = query.get('v', [''])[0]

        if vid_id:
            try:
                captions = YouTubeTranscriptApi.get_transcript(vid_id)
                transcript = ' '.join(entry['text'] for entry in captions) if captions else "Transcript not available"

                # Assuming you have 'transcript' containing the text you want to summarize
                original_text = transcript

                # Create a plaintext parser
                parser = PlaintextParser.from_string(original_text, Tokenizer("english"))

                # Create a summarizer
                summarizer = LsaSummarizer(Stemmer("english"))

                # Get the summary
                summary = summarizer(parser.document, 8)  # Change '5' to the number of sentences you want in the summary

                # Convert the summary to a string
                summary_text = " ".join([str(sentence) for sentence in summary])

            except Exception as e:
                summary_text = "Error: " + str(e)

    return render_template('index.html', transcript=transcript, summary=summary_text)


if __name__ == '__main__':
    app.run()
