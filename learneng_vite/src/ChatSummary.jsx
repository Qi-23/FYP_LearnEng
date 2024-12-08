import { useEffect, useState, useRef } from "react";

function ChatSummary() {

  const [loading, setLoading] = useState(false);
  const summarizedRef = useRef(false);
  const generating = useRef(false);

  const getSummary = async () => {
    if (!summarizedRef.current) {
      setLoading(true);
      summarizedRef.current = true;
      generating.current = true;
      $("#summary-area").removeClass("d-none");
      const response = await fetch("/api/SummarizeContent");
      let formattedResponse = ""
      if (response.ok) {
        // $("#summary-area").removeClass("d-none");
        const data = (await response.json()).summarized_content;
        formattedResponse = data.replace(/\n/g, '</br>');
        formattedResponse = formattedResponse.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formattedResponse = formattedResponse.replace(/\*([\s\S]+?)<\/br>/g, '<ul class="list-dot"><li>$1</li></ul>');
        formattedResponse = formattedResponse.replace(/\+([\s\S]+?)<\/br>/g, '<ul class="list-circle" style="padding-left: 20px;"><li>$1</li></ul>');
        setLoading(false);
        $("#summarizedContent").html(formattedResponse);
      }
      generating.current = false;
      setLoading(false);
    }
  };

  const summarizeAgain = () => {
    if (!generating.current) {
      summarizedRef.current = false;
      getSummary();
    }
  }

  useEffect(() => {
    if (loading) {
      $("#summarizedContent").html("<div class='h-100 d-flex justify-content-center'><img style='width: 200px' src='page_photo/ripples.svg'></div>");
    } else {
      $("#summarizedContent img").remove();
    }
  }, [loading]);

  useEffect(() => {
    const summary_btn = document.querySelector('.summary-btn');
    const summary_again_btn = document.querySelector('#btn-summarize_again');
    summary_btn.addEventListener('click', getSummary);
    summary_again_btn.addEventListener('click', summarizeAgain);

    return () => {
      summary_btn.removeEventListener('click', getSummary);
      summary_again_btn.removeEventListener('click', summarizeAgain);
    };
  }, []);

  return (
    <>
    </>
  );
}

export default ChatSummary;