import { useEffect, useState } from "react";

function ChatSummary() {

  const getSummary = async () => {
    $("#summary-area").removeClass("d-none");
    const response = await fetch("/api/SummarizeContent");
    let formattedResponse = ""
    console.log("send");
    if (response.ok) {
      $("#summary-area").removeClass("d-none");
      const data = (await response.json()).summarized_content;
      formattedResponse = data.replace(/\n/g, '</br>');
      formattedResponse = formattedResponse.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      formattedResponse = formattedResponse.replace(/\*([\s\S]+?)<\/br>/g, '<ul class="list-dot"><li>$1</li></ul>');
      formattedResponse = formattedResponse.replace(/\+([\s\S]+?)<\/br>/g, '<ul class="list-circle" style="padding-left: 20px;"><li>$1</li></ul>');
      $("#summarizedContent").html(formattedResponse);
    }
  };

  useEffect(() => {
    const button = document.querySelector('.summary-btn');
    button.addEventListener('click', getSummary);

    return () => {
      button.removeEventListener('click', getSummary);
    };
  }, []);

  return (
    <>
    </>
  );
}

export default ChatSummary;