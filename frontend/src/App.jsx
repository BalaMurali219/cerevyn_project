import { useState, useEffect } from 'react'
import './App.css'
import { submitLead, checkHealth } from './api'

function App() {
  const [leadData, setLeadData] = useState({
    Name: '',
    Phone: '',
    Email: '',
    InterestLevel: 'Auto Predict',
    Age: 35,
    Gender: 'Female',
    Location: 'Lahore',
    LeadSource: 'Email',
    TimeSpent: 12,
    PagesViewed: 3,
    LeadStatus: 'Warm',
    EmailSent: 2,
    DeviceType: 'Desktop',
    ReferralSource: 'Direct',
    FormSubmissions: 1,
    Downloads: 0,
    CTR_ProductPage: 0.1,
    ResponseTime: 5,
    FollowUpEmails: 2,
    SocialMediaEngagement: 50,
    PaymentHistory: 'None'
  })

  const [workflowEvents, setWorkflowEvents] = useState([])
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [backendHealth, setBackendHealth] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    checkHealth()
      .then(res => setBackendHealth(res))
      .catch(err => setBackendHealth({ status: 'error', message: err.message }))
  }, [])

  const handleChange = (e) => {
    const { name, value, type } = e.target
    setLeadData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setWorkflowEvents([])
    setPrediction(null)
    
    try {
      const result = await submitLead(leadData)
      if (result.error) {
        setError(result.error)
      } else {
        setPrediction({
          score: result.probability,
          intent: result.prediction === 1 ? 'High Intent (Will Convert)' : 'Low/Medium Intent'
        })
        
        // Stagger events to simulate workflow orchestration
        result.workflow_events.forEach((event, idx) => {
          setTimeout(() => {
            setWorkflowEvents(prev => [...prev, event])
          }, idx * 800)
        })
      }
    } catch (err) {
      setError("Failed to process lead. Please ensure backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>Intelligent Workflow Automation</h1>
        <div className={`status ${backendHealth?.status === 'ok' ? 'online' : 'offline'}`}>
          Backend Status: {backendHealth ? (backendHealth.model_loaded ? 'Online & Model Loaded' : 'Online (Train Model Required)') : 'Connecting...'}
        </div>
      </header>

      <main className="main-content">
        <div className="card form-card">
          <h2>New Lead Entry</h2>
          <form onSubmit={handleSubmit} className="lead-form">
            <div className="form-group">
              <label>Name:</label>
              <input type="text" name="Name" value={leadData.Name} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Phone:</label>
              <input type="tel" name="Phone" value={leadData.Phone} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input type="email" name="Email" value={leadData.Email} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Predicted Interest Override:</label>
              <select name="InterestLevel" value={leadData.InterestLevel} onChange={handleChange}>
                <option value="Auto Predict">Auto Predict (ML)</option>
                <option value="High">High Intent</option>
                <option value="Medium">Medium Intent</option>
                <option value="Low">Low Intent</option>
              </select>
            </div>
            <div className="form-group">
              <label>Age:</label>
              <input type="number" name="Age" value={leadData.Age} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Time Spent (mins):</label>
              <input type="number" name="TimeSpent" value={leadData.TimeSpent} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Pages Viewed:</label>
              <input type="number" name="PagesViewed" value={leadData.PagesViewed} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>CTR Product Page:</label>
              <input type="number" step="0.01" name="CTR_ProductPage" value={leadData.CTR_ProductPage} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Lead Source:</label>
              <select name="LeadSource" value={leadData.LeadSource} onChange={handleChange}>
                <option value="Email">Email</option>
                <option value="Referral">Referral</option>
                <option value="Organic">Organic</option>
                <option value="SocialMedia">Social Media</option>
              </select>
            </div>
            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Processing...' : 'Ingest Lead & Trigger Workflow'}
            </button>
          </form>
          {error && <div className="error-msg">{error}</div>}
        </div>

        <div className="card workflow-card">
          <h2>Workflow Orchestrator Dashboard</h2>
          
          {prediction && (
            <div className="prediction-box">
              <h3>ML Prediction Engine</h3>
              <p>Conversion Score: {(prediction.score * 100).toFixed(1)}%</p>
              <p>Classification: {prediction.intent}</p>
            </div>
          )}

          <div className="events-timeline">
            <h3>Execution Trace</h3>
            {workflowEvents.length === 0 && !loading && <span className="empty-text">Waiting for triggers...</span>}
            {workflowEvents.map((event, i) => (
              <div key={i} className="event-item slide-in">
                <span className="step-badge">Step {event.step}</span>
                <span className="event-action">{event.action}</span>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
