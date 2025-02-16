import React, { useState } from "react";
import axios from "axios";

const CheckAppointment = () => {
  const [appointmentId, setAppointmentId] = useState("");
  const [appointmentDetails, setAppointmentDetails] = useState(null);
  const [error, setError] = useState("");

  const fetchAppointment = async () => {
    try {
      setError("");
      setAppointmentDetails(null);
  
      // Ensure appointmentId is not empty
      if (!appointmentId.trim()) {
        setError("Please enter a valid Appointment ID.");
        return;
      }
  
      const response = await axios.get(
        `https://6pa521b853.execute-api.us-west-2.amazonaws.com/dev/checkappointment/${appointmentId}`,
        {
          headers: { "Content-Type": "application/json" },
        }
      );
  
      // Debugging: Print response data
      console.log("API Response:", response.data);
  
      // Check if response is valid
      if (response.status === 200 && response.data) {
        setAppointmentDetails(response.data);
      } else {
        setError("Appointment not found.");
        console.error("Error: No appointment data returned");
      }
    } catch (err) {
      // Debugging: Print full error details
      console.error("API Request Error:", err);
  
      if (err.response) {
        console.error("Response Data:", err.response.data);
        console.error("Response Status:", err.response.status);
        console.error("Response Headers:", err.response.headers);
        setError(`Error: ${err.response.data.error || "Appointment not found."}`);
      } else if (err.request) {
        console.error("Request Details:", err.request);
        setError("No response received from the server. Please try again.");
      } else {
        console.error("Error Message:", err.message);
        setError("An error occurred while fetching the appointment.");
      }
  
      setAppointmentDetails(null);
    }
  };
  

  return (
    <div>
      <h2>Check Your Appointment</h2>
      <input
        type="text"
        placeholder="Enter Appointment ID"
        onChange={(e) => setAppointmentId(e.target.value)}
      />
      <button onClick={fetchAppointment}>Check Status</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {appointmentDetails && (
        <div>
          <h3>Appointment Details</h3>
          <p><strong>ID:</strong> {appointmentDetails.appointment_id}</p>
          <p><strong>Name:</strong> {appointmentDetails.user_name}</p>
          <p><strong>Date:</strong> {appointmentDetails.appointment_date}</p>
          <p><strong>Time:</strong> {appointmentDetails.appointment_time}</p>
          <p><strong>Reason:</strong> {appointmentDetails.reason}</p>
        </div>
      )}
    </div>
  );
};

export default CheckAppointment;
