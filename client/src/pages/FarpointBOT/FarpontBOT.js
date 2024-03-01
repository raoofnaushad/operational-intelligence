import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import FarpointSidebar from "../../components/FarpointSidebar/FarpointSidebar";
import "./FarpointBOT.css";

const FarpointBOT = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false); // New state for loading indicator
  const apiUrl = process.env.REACT_APP_API_URL;

  // Retrieve token and user info from local storage
  const token = localStorage.getItem("access_token");
  const userInfo = JSON.parse(localStorage.getItem("userInfo") || "{}");
  const userId = userInfo.userId;

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  const fetchChatHistory = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `${apiUrl}/farpointbot/chat_history?userid=${userId}`,
        {
          method: "GET",
          credentials: "include",
          mode: "cors",
          headers: {
            // Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const chatHistory = await response.json();

      // Update the messages state with the fetched chat history
      setMessages(
        chatHistory.map((chat) => ({
          sender: chat.generated_by === "user" ? "user" : "Chaplin",
          text: chat.text,
        }))
      );

      console.log(chatHistory);

      setIsLoading(false);
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (inputText.trim() === "") return;

    // Add user's message
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: "user", text: inputText },
    ]);

    setIsLoading(true); // Start loading

    // Prepare the data to send, now including the userId
    const requestData = {
      user_input: inputText,
      userid: userId, // Include the userId in the request data
    };

    try {
      // Send API request to backend
      const response = await fetch(`${apiUrl}/farpointbot/bot_response`, {
        method: "POST",
        credentials: "include",
        mode: "cors",
        headers: {
          // Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Get the response data
      const responseData = await response.json();

      // Assuming responseData contains a field 'bot_response' with the bot's reply
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "Chaplin", text: responseData.bot_response },
      ]);
      setIsLoading(false);
    } catch (error) {
      console.error("Error sending message to bot:", error);
      setIsLoading(false); // Stop loading in case of error
    }

    // Clear input field
    setInputText("");
  };

  // useEffect hook to fetch chat history when the component mounts
  useEffect(() => {
    fetchChatHistory();
  }, []); // Empty dependency array means this runs once on component mount

  return (
    <div className="app">
      <FarpointSidebar />
      <div className="chat-container">
        <div className="chat-window">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${
                message.sender === "user" ? "user-message" : "bot-message"
              }`}
            >
              <div className="message-sender">
                {message.sender === "user" ? "User" : "Chaplin"}
              </div>
              <ReactMarkdown>{message.text}</ReactMarkdown>
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={inputText}
            onChange={handleInputChange}
            placeholder="Ask Chaplin..."
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || inputText.trim() === ""}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
export default FarpointBOT;
