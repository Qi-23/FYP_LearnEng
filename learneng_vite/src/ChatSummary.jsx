import { useEffect, useState, useRef } from "react";

function ChatSummary() {

  const [loading, setLoading] = useState(false);
  const summarizedRef = useRef(false);

  const queryParams = new URLSearchParams(window.location.search);
  const id = queryParams.get("id");

  const getSummary = async () => {
    if (!summarizedRef.current) {
      setLoading(true);
      summarizedRef.current = true;
      console.log("summarizing")
      $("#summary-area").removeClass("d-none");
        const response = await fetch("/api/SummarizeContent", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id: id })
        });
    

      let formattedResponse = ""
      if (response.ok) {
        data = await response.json()
        const summary = data.summarized_content;
        formattedResponse = summary.replace(/\n/g, '</br>');
        formattedResponse = formattedResponse.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formattedResponse = formattedResponse.replace(/\*([\s\S]+?)(?:<\/br>|$)/g, '<ul class="mb-0 list-dot"><li>$1</li></ul>');
        formattedResponse = formattedResponse.replace(/\+([\s\S]+?)<\/br>/g, '<ul class="mb-0 list-circle" style="padding-left: 20px;"><li>$1</li></ul>');
        formattedResponse = formattedResponse.replace(/â€™/g, "'");
        setLoading(false);
        $("#summarizedContent").html(formattedResponse);
      }
      setLoading(false);
    }
  };

  useEffect(() => {
    if (loading) {
      $("#summarizedContent").html("<div class='h-100 d-flex justify-content-center'><img style='width: 200px' src='page_photo/ripples.svg'></div>");
    } else {
      $("#summarizedContent img").remove();
    }
  }, [loading]);

  useEffect(() => {
    const summary_btn = document.querySelector('.summary-btn');
    summary_btn.addEventListener('click', getSummary);

    return () => {
      summary_btn.removeEventListener('click', getSummary);
    };
  }, []);

  return (
    <>
    </>
  );
}

export default ChatSummary;