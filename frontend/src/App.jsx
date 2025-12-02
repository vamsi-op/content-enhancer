import { useState, useEffect, useRef } from 'react'
import './App.css'
import './themes/style.css'
import AuditForm from './components/AuditForm'
import ResultsDashboard from './components/ResultsDashboard'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [showHistory, setShowHistory] = useState(false)
  const [showTips, setShowTips] = useState(false)
  const resultsRef = useRef(null)

  // Load history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('audit_history')
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory))
      } catch (e) {
        console.error('Failed to load history:', e)
      }
    }
    
    // Keyboard shortcuts
    const handleKeyPress = (e) => {
      // Ctrl/Cmd + K to focus search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault()
        document.querySelector('textarea')?.focus()
      }
      // Ctrl/Cmd + H to toggle history
      if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
        e.preventDefault()
        setShowHistory(prev => !prev)
      }
      // ? to show tips
      if (e.key === '?' && !e.ctrlKey && !e.metaKey && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault()
        setShowTips(prev => !prev)
      }
    }
    
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [])

  // Auto-scroll to results when they appear
  useEffect(() => {
    if (results && resultsRef.current) {
      resultsRef.current.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
      })
    }
  }, [results])

  const API_URL = import.meta.env.VITE_API_URL || (import.meta.env.MODE === 'production' ? '/api' : 'http://localhost:5000/api')

  const handleAnalyze = async (inputData) => {
    setLoading(true)
    setError(null)
    setResults(null)
    
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputData)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Analysis failed')
      }
      
      const data = await response.json()
      
      if (data.error) {
        throw new Error(data.error)
      }
      
      setResults(data)
      
      // Save to history
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        score: data.overall_score,
        input: inputData.input.substring(0, 100) + '...',
        isUrl: inputData.is_url,
        results: data  // Save full results for later viewing
      }
      const newHistory = [historyItem, ...history].slice(0, 10) // Keep last 10
      setHistory(newHistory)
      localStorage.setItem('audit_history', JSON.stringify(newHistory))
    } catch (err) {
      console.error('Analysis error:', err)
      setError(err.message || 'Failed to analyze content. Please check if the backend server is running.')
    }
    setLoading(false)
  }

  return (
    <div className="app">
      <header>
        <div className="header-content">
          <div>
            <h1>🎯 Content Quality Audit Tool</h1>
            <p>Analyze content across 5 dimensions with AI-powered insights</p>
          </div>
          <div className="header-actions">
            <button 
              className="history-toggle"
              onClick={() => setShowHistory(!showHistory)}
            >
              📊 History {history.length > 0 && `(${history.length})`}
            </button>
            <button 
              className="tips-toggle"
              onClick={() => setShowTips(!showTips)}
              title="Show keyboard shortcuts"
            >
              ⌨️ Tips
            </button>
          </div>
        </div>
      </header>
      
      {/* Tips Modal */}
      {showTips && (
        <div className="modal-overlay" onClick={() => setShowTips(false)}>
          <div className="tips-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>💡 Pro Tips & Shortcuts</h3>
              <button onClick={() => setShowTips(false)}>✕</button>
            </div>
            <div className="tips-content">
              <div className="tip-section">
                <h4>⌨️ Keyboard Shortcuts</h4>
                <div className="shortcut-list">
                  <div className="shortcut-item">
                    <kbd>Ctrl/Cmd + K</kbd>
                    <span>Focus input field</span>
                  </div>
                  <div className="shortcut-item">
                    <kbd>Ctrl/Cmd + H</kbd>
                    <span>Toggle history</span>
                  </div>
                  <div className="shortcut-item">
                    <kbd>?</kbd>
                    <span>Show this help</span>
                  </div>
                </div>
              </div>
              
              <div className="tip-section">
                <h4>✨ Pro Tips</h4>
                <ul className="tips-list">
                  <li>Aim for 800-2000 words for optimal SEO</li>
                  <li>Use headers (H1, H2, H3) to structure content</li>
                  <li>Include your target keyword 1-2% of the time</li>
                  <li>Vary sentence length for better readability</li>
                  <li>Add unique examples and personal insights</li>
                  <li>Export results to track improvement over time</li>
                </ul>
              </div>
              
              <div className="tip-section">
                <h4>🎯 Quick Actions</h4>
                <ul className="tips-list">
                  <li>Paste text or URL - auto-detected!</li>
                  <li>Click score cards to expand/collapse</li>
                  <li>Use AI buttons for instant improvements</li>
                  <li>Export as JSON or HTML report</li>
                  <li>Share results with your team</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* History Sidebar */}
      {showHistory && (
        <div className="history-sidebar">
          <div className="history-header">
            <h3>📊 Recent Analyses</h3>
            <button onClick={() => setShowHistory(false)}>✕</button>
          </div>
          {history.length > 0 ? (
            <>
              <div className="history-list">
                {history.map(item => (
                  <div 
                    key={item.id} 
                    className={`history-item ${!item.results ? 'disabled' : ''}`}
                    onClick={() => {
                      // Load the full results from history
                      if (item.results) {
                        setResults(item.results)
                        setShowHistory(false)
                      } else {
                        alert('⚠️ This history item was saved before full results storage was enabled. Please run a new analysis to save complete results.')
                      }
                    }}
                    style={{ cursor: 'pointer' }}
                    title={item.results ? "Click to view this analysis" : "Old history item - results not available"}
                  >
                    <div className="history-score">{item.score.toFixed(0)}</div>
                    <div className="history-details">
                      <div className="history-preview">{item.input}</div>
                      <div className="history-time">
                        {new Date(item.timestamp).toLocaleDateString()} {new Date(item.timestamp).toLocaleTimeString()}
                        {!item.results && <span style={{color: '#ef4444', marginLeft: '8px'}}>⚠️ No data</span>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <button 
                className="clear-history-btn"
                onClick={() => {
                  if (confirm('Clear all history?')) {
                    setHistory([])
                    localStorage.removeItem('audit_history')
                  }
                }}
              >
                🗑️ Clear History
              </button>
            </>
          ) : (
            <div className="empty-history">
              <div className="empty-icon">📭</div>
              <h4>No History Yet</h4>
              <p>Your analysis history will appear here once you start auditing content.</p>
              <div className="empty-tips">
                <p>💡 Tip: History is saved automatically and persists across sessions.</p>
              </div>
            </div>
          )}
        </div>
      )}
      
      <AuditForm 
        onAnalyze={handleAnalyze} 
        loading={loading}
      />
      {loading && <div className="loading">⏳ Analyzing...</div>}
      {error && (
        <div className="error-banner">
          <h3>⚠️ Error</h3>
          <p>{error}</p>
        </div>
      )}
      {results && (
        <div ref={resultsRef}>
          <ResultsDashboard results={results} />
        </div>
      )}
    </div>
  )
}

export default App
