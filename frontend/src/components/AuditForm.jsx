import { useState } from 'react'

export default function AuditForm({ onAnalyze, loading }) {
  const [input, setInput] = useState('')
  const [keyword, setKeyword] = useState('')

  // Auto-detect if input is a URL
  const isUrl = (text) => {
    try {
      const trimmed = text.trim()
      return trimmed.startsWith('http://') || trimmed.startsWith('https://')
    } catch {
      return false
    }
  }

  // Calculate stats
  const wordCount = input.trim().split(/\s+/).filter(w => w.length > 0).length
  const charCount = input.length
  const estimatedReadTime = Math.ceil(wordCount / 200)
  const isUrlInput = isUrl(input)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      const inputTrimmed = input.trim()
      onAnalyze({ 
        input: inputTrimmed, 
        target_keyword: keyword.trim(),
        is_url: isUrl(inputTrimmed)
      })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="audit-form">
      <div className="form-group">
        <label>
          Enter Content or URL:
          <span className="hint">Paste text or start with http:// for URL analysis</span>
        </label>
        <textarea 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Paste your content here or enter a URL (https://example.com/article)..."
          rows="8"
          required
        />
        {input && !isUrlInput && (
          <div className="input-stats">
            <span className="stat-item">
              {wordCount} words
            </span>
            <span className="stat-item">
              {charCount} characters
            </span>
            <span className="stat-item">
              ~{estimatedReadTime} min read
            </span>
            <span className={`stat-item ${wordCount < 300 ? 'warning' : wordCount > 2000 ? 'warning' : 'success'}`}>
              {wordCount < 300 ? 'Too short' : wordCount > 2000 ? 'Very long' : 'Good length'}
            </span>
          </div>
        )}
      </div>
      
      <div className="form-group">
        <label>Target Keyword (optional):</label>
        <input 
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="e.g., 'best budget laptops 2025'"
        />
      </div>

      <button type="submit" disabled={loading} className="analyze-btn">
        {loading ? 'Analyzing...' : 'Analyze Content'}
      </button>
    </form>
  )
}
