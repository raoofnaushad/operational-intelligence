import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";

import FarpointSidebar from "../../components/FarpointSidebar/FarpointSidebar";

import "./ArchivedMeeting.css";

const ArchivedMeeting = () => {
  const apiUrl = process.env.REACT_APP_API_URL;

  const [meetingDetails, setMeetingDetails] = useState({
    attendees: "",
    date: "",
    interviewType: "",
    companyName: "",
  });
  const [newQuestion, setNewQuestion] = useState("");
  const [questions, setQuestions] = useState([]);
  const { meeting_id } = useParams();
  const navigate = useNavigate();
  const [visibleAnswers, setVisibleAnswers] = useState({});
  const [isEditing, setIsEditing] = useState(false);
  const [editableMeetingSummary, setEditableMeetingSummary] = useState(
    meetingDetails.meetingSummary
  );

  useEffect(() => {
    const fetchMeetingDetails = async () => {
      try {
        const response = await fetch(
          `${apiUrl}/interview/get_interview_details/${meeting_id}`,
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
          if (response.status === 401) {
            // Navigate to login page only if response status is 401 (Unauthorized)
            navigate("/login");
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonResponse = await response.json();
        console.log("Interview details:", jsonResponse);

        // Adjusted to accommodate the actual response format
        const details = jsonResponse.interviewDetails; // Access the nested interviewDetails object
        setMeetingDetails({
          attendees: details.attendees, // No need to check for array as it's a string
          date: details.date,
          interviewType: details.interviewType,
          companyName: details.companyName,
          meetingSummary: details.meeting_summary,
        });
      } catch (error) {
        console.error("Error fetching interview details:", error);
      }
    };

    fetchMeetingDetails();
  }, [meeting_id, navigate]);

  useEffect(() => {
    const fetchInterviewQuestions = async () => {
      try {
        const response = await fetch(
          `${apiUrl}/interview/get_interview_questions/${meeting_id}`,
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
        const jsonResponse = await response.json();

        console.log("Interview questions:", jsonResponse.questions);
        setQuestions(jsonResponse.questions);
      } catch (error) {
        console.error("Error fetching interview questions:", error);
      }
    };

    fetchInterviewQuestions();
  }, [meeting_id, apiUrl]); // Dependency array ensures fetch runs when these values change

  const handleAnswerVisibilityChange = (index) => {
    setVisibleAnswers((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const addQuestionToBackend = async (newQuestion) => {
    if (newQuestion.trim() === "") {
      console.error("Question is empty.");
      return;
    }

    try {
      const response = await fetch(
        `${apiUrl}/interview/add_interview_questions/${meeting_id}`,
        {
          method: "POST",
          credentials: "include",
          mode: "cors",
          headers: {
            // Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question: newQuestion, answered: false }), // Adjust based on your backend expectations
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const jsonResponse = await response.json();
      console.log("Add question response:", jsonResponse);

      // Optionally update your local state to reflect the added question
      setQuestions((prevQuestions) => [
        ...prevQuestions,
        { question: newQuestion, answered: false },
      ]);
      setNewQuestion("");
    } catch (error) {
      console.error("Error adding new question:", error);
      // Handle error state appropriately (e.g., show an error message to the user)
    }
  };

  const toggleEdit = () => {
    if (!isEditing) {
      // Move this line inside the if block so it updates only when entering edit mode
      setEditableMeetingSummary(meetingDetails.meetingSummary);
    }
    setIsEditing(!isEditing);
  };

  const saveEdit = async () => {
    try {
      // Assuming apiUrl is already defined in your component
      const response = await fetch(
        `${apiUrl}/interview/update_meeting_notes/${meeting_id}`,
        {
          method: "POST",
          credentials: "include",
          mode: "cors",
          headers: {
            // Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ meetingSummary: editableMeetingSummary }), // Adjust based on your backend expectations
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const jsonResponse = await response.json();
      console.log("Update response:", jsonResponse);

      // Update the local state to reflect the saved changes
      setMeetingDetails((prevDetails) => ({
        ...prevDetails,
        meetingSummary: editableMeetingSummary,
      }));

      setIsEditing(false); // Exit editing mode
    } catch (error) {
      console.error("Error saving meeting notes:", error);
      // Handle error state appropriately (e.g., show an error message to the user)
    }
  };

  const updateQuestionStatus = async (questionIndex, questionId, action) => {
    const currentValid = questions[questionIndex].valid;

    let newValid;
    if (action === "like") {
      // If current state is liked (1), change to neutral (0); otherwise, change to liked (1)
      newValid = currentValid === 1 ? 0 : 1;
    } else if (action === "dislike") {
      // If current state is disliked (-1), change to neutral (0); otherwise, change to disliked (-1)
      newValid = currentValid === -1 ? 0 : -1;
    }

    try {
      const response = await fetch(
        `${apiUrl}/interview/update_question_status/${meeting_id}/${questionId}`,
        {
          method: "PATCH",
          credentials: "include",
          mode: "cors",
          headers: {
            // Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ valid: newValid }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Update the local state to reflect the action
      setQuestions((currentQuestions) =>
        currentQuestions.map((q, index) =>
          index === questionIndex ? { ...q, valid: newValid } : q
        )
      );
    } catch (error) {
      console.error(`Error updating question status: ${error}`);
    }
  };

  return (
    <div className="archived-container">
      <FarpointSidebar />
      <div className="archived-meeting">
        <div className="meeting-header">
          <div className="header-content">
            <h1>{meetingDetails.companyName}</h1>
            <p>
              <span className="detail-key">Attendees:</span>{" "}
              {meetingDetails.attendees}
            </p>
            <p>
              <span className="detail-key">Date:</span> {meetingDetails.date}
            </p>
            <p>
              <span className="detail-key">Interview Type:</span>{" "}
              {meetingDetails.interviewType}
            </p>
          </div>
          <button className="follow-up-btn">Send follow up email</button>
        </div>
        <div className="meeting-content">
          <div className="questions-container">
            <div className="questions-list">
              <h2>Recommended Questions and Answers</h2>
              {questions.map((q, index) => (
                <div key={index} className="question">
                  <div className="question-title">{q.question}</div>
                  <button
                    onClick={() => handleAnswerVisibilityChange(index)}
                    disabled={!q.answered}
                    className={`toggle-btn ${!q.answered ? "disabled" : ""} ${
                      visibleAnswers[index] ? "show" : ""
                    }`}
                  >
                    {visibleAnswers[index] ? "Hide Answer" : "Show Answer"}
                  </button>
                  <button
                    onClick={() => updateQuestionStatus(index, q.id, "like")}
                    className={`like-btn ${q.valid === 1 ? "liked" : ""}`}
                  >
                    <i
                      className={`fas fa-thumbs-up ${
                        q.valid === 1 ? "active" : ""
                      }`}
                    ></i>
                  </button>
                  <button
                    onClick={() => updateQuestionStatus(index, q.id, "dislike")}
                    className={`delete-btn ${q.valid === -1 ? "disliked" : ""}`}
                  >
                    <i
                      className={`fas fa-thumbs-down ${
                        q.valid === -1 ? "active" : ""
                      }`}
                    ></i>
                  </button>
                  {visibleAnswers[index] && (
                    <div className="question-answer">{q.answer}</div>
                  )}
                </div>
              ))}
            </div>
            <div className="question-input">
              <input
                type="text"
                value={newQuestion}
                onChange={(e) => setNewQuestion(e.target.value)}
                placeholder="Add a new question"
              />
              <button onClick={() => addQuestionToBackend(newQuestion)}>
                Enter
              </button>
            </div>
          </div>
          <div className="meeting-notes">
            <h2>Meeting Notes</h2>
            {isEditing ? (
              <textarea
                value={editableMeetingSummary}
                onChange={(e) => setEditableMeetingSummary(e.target.value)}
              />
            ) : (
              <pre>{meetingDetails.meetingSummary}</pre>
            )}
            <div>
              {isEditing ? (
                <button onClick={saveEdit} className="save-btn">
                  Save
                </button>
              ) : (
                <button onClick={toggleEdit} className="edit-btn">
                  Edit
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArchivedMeeting;
