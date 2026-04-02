import { useState, useEffect } from "react";

export default function ChatInterface() {
  const [messages, setMessages] = useState<Array<{ role: string; content: string; timestamp?: string }>>([]);
  const [input, setInput] = useState("");

  const loadHistory = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
      const res = await fetch(`${apiUrl}/api/chat/history`);
      if (!res.ok) {
        throw new Error(`History fetch failed: ${res.status}`);
      }
      const data = await res.json();
      if (data.history) {
        setMessages(data.history.map((m: any) => ({ role: m.role, content: m.content, timestamp: m.timestamp })));
      }
    } catch (err) {
      console.error("Failed to load chat history", err);
      setMessages([{ role: "assistant", content: "Welcome to FinAlly! Ask me anything about your portfolio." }]);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }] );

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
      const response = await fetch(`${apiUrl}/api/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Chat request failed");
      }

      const reply = data.response || "Agent không trả lời được.";
      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);

      if (data.trade_executed) {
        const trade = data.trade_executed.trade;
        setMessages((prev) => [...prev, {
          role: "assistant",
          content: `Trade executed: ${trade.action.toUpperCase()} ${trade.ticker} x${trade.quantity} @ ${trade.price}`
        }]);
      }

    } catch (error: any) {
      const err = error?.message || "Unknown error";
      setMessages((prev) => [...prev, { role: "assistant", content: `Error: ${err}` }]);
      console.error("Chat API error", err);
    } finally {
      setInput("");
    }
  };

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800 p-4">
      <h2 className="text-lg font-bold text-white mb-3">AI Chat</h2>
      <div className="h-48 overflow-y-auto rounded-lg bg-gray-900 p-3 mb-3">
        {messages.length === 0 ? (
          <p className="text-sm text-gray-400">No history yet.</p>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`mb-2 ${msg.role === "user" ? "text-right" : "text-left"}`}>
              <div className={`inline-block rounded-lg p-2 ${msg.role === "user" ? "bg-blue-600" : "bg-gray-700"}`}>
                <span className="text-sm text-white">{msg.content}</span>
                {msg.timestamp && <div className="text-xs text-gray-300 mt-1">{new Date(msg.timestamp).toLocaleTimeString()}</div>}
              </div>
            </div>
          ))
        )}
      </div>
      <div className="flex gap-2">
        <input
          id="chat-message"
          name="chat-message"
          className="flex-1 rounded-lg border border-gray-600 bg-gray-900 p-2 text-white"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask portfolio advice..."
          autoComplete="off"
        />
        <button onClick={sendMessage} className="rounded-lg bg-blue-500 px-4 py-2 text-white">Send</button>
      </div>
    </div>
  );
}