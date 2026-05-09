import React, { useState } from "react";
import axios from "axios";

export default function App() {

  const [input, setInput] = useState("");
  const [reply, setReply] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    setLoading(true);

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          messages: [
            {
              role: "user",
              content: input
            }
          ]
        }
      );

      setReply(res.data);

    } catch (err) {

      setReply({
        reply: "Something went wrong while contacting the backend.",
        recommendations: []
      });

    } finally {

      setLoading(false);
    }
  };

  return (
    <div style={{
      background:"#020617",
      minHeight:"100vh",
      color:"white",
      fontFamily:"Arial",
      padding:"40px"
    }}>

      <h1 style={{
        fontSize:"52px",
        fontWeight:"bold"
      }}>
        SHL Conversational Assessment Recommender
      </h1>

      <div style={{
        marginTop:"30px",
        background:"#1e293b",
        padding:"30px",
        borderRadius:"20px"
      }}>

        <textarea
          rows="5"
          value={input}
          onChange={(e)=>setInput(e.target.value)}
          placeholder="Describe hiring requirements..."
          style={{
            width:"100%",
            borderRadius:"16px",
            padding:"20px",
            fontSize:"18px"
          }}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          style={{
            marginTop:"20px",
            background:"#38bdf8",
            padding:"14px 28px",
            border:"none",
            borderRadius:"12px",
            fontSize:"18px",
            cursor:"pointer",
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? "Loading..." : "Get Recommendations"}
        </button>
      </div>

      {reply && (
        <div style={{
          marginTop:"30px",
          background:"#1e293b",
          padding:"30px",
          borderRadius:"20px"
        }}>

          <h2>Assistant Reply</h2>

          <p>{reply.reply}</p>

          <h2 style={{marginTop:"20px"}}>
            Recommendations
          </h2>

          {
            reply.recommendations &&
            reply.recommendations.length === 0 && (
              <p>No recommendations available.</p>
            )
          }

          {
            reply.recommendations &&
            reply.recommendations.length > 0 &&
            reply.recommendations.map((r, i)=>(
              <div
                key={i}
                style={{
                  background:"#334155",
                  padding:"20px",
                  borderRadius:"14px",
                  marginTop:"20px"
                }}
              >

                <h3>{r.name}</h3>

                <p>Type: {r.test_type}</p>

                <a
                  href={r.url}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    color:"#38bdf8"
                  }}
                >
                  Open Assessment
                </a>

              </div>
            ))
          }

        </div>
      )}

    </div>
  );
}