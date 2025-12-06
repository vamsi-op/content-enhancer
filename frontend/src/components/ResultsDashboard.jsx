import { useState } from 'react'

const Tooltip = ({ text, children }) => {
  const [show, setShow] = useState(false)
  
  return (
    <span 
      className="tooltip-wrapper"
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
    >
      {children}
      {show && <div className="tooltip-box">{text}</div>}
    </span>
  )
}

export default function ResultsDashboard({ results }) {
  // Safety check - ensure results and scores exist
  if (!results || !results.scores) {
    return (
      <div className="results-dashboard">
        <div className="error-message">
          <h3>Error Loading Results</h3>
          <p>Unable to load analysis results. Please try again.</p>
        </div>
      </div>
    )
  }

  const scores = results.scores
  const [aiImproving, setAiImproving] = useState(false)
  const [improvedContent, setImprovedContent] = useState(null)
  const [copyButtonText, setCopyButtonText] = useState('Copy to Clipboard')

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981'
    if (score >= 60) return '#f59e0b'
    return '#ef4444'
  }

  // Export functions
  const exportAsJSON = () => {
    const dataStr = JSON.stringify(results, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `content-audit-${Date.now()}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const exportAsHTML = () => {
    const html = `
<!DOCTYPE html>
<html>
<head>
  <title>Content Audit Report</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
    .header { background: linear-gradient(135deg, #10a37f, #0d8f6f); color: white; padding: 40px; border-radius: 12px; text-align: center; }
    .score { font-size: 3em; font-weight: bold; margin: 20px 0; }
    .section { background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .metric { display: inline-block; margin: 10px 20px; text-align: center; }
    .metric-value { font-size: 2em; color: #10a37f; font-weight: bold; }
    .issue { color: #ef4444; margin: 10px 0; }
    .recommendation { color: #3b82f6; margin: 10px 0; }
    h2 { color: #333; border-bottom: 2px solid #10a37f; padding-bottom: 10px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Content Quality Audit Report</h1>
    <div class="score">${results.overall_score.toFixed(1)}/100</div>
    <p>Generated on ${new Date().toLocaleDateString()}</p>
  </div>
  
  <div class="section">
    <h2>Content Metrics</h2>
    ${scores.seo?.details?.content_metrics ? `
      <div class="metric"><div class="metric-value">${scores.seo.details.content_metrics.word_count}</div><div>Words</div></div>
      <div class="metric"><div class="metric-value">${scores.seo.details.content_metrics.reading_time_minutes}</div><div>Min Read</div></div>
      <div class="metric"><div class="metric-value">${scores.seo.details.content_metrics.paragraph_count}</div><div>Paragraphs</div></div>
    ` : ''}
  </div>
  
  <div class="section">
    <h2>Analysis Scores</h2>
    <p><strong>SEO:</strong> ${scores.seo.score}/100</p>
    <p><strong>SERP Performance:</strong> ${scores.serp.score}/100</p>
    <p><strong>AEO Readiness:</strong> ${scores.aeo.score}/100</p>
    <p><strong>Humanization:</strong> ${scores.humanization.score}/100</p>
    <p><strong>Differentiation:</strong> ${scores.differentiation.score}/100</p>
  </div>
  
  <div class="section">
    <h2>Strengths - What's Working Well</h2>
    ${scores.seo.details?.good_points?.map(point => `<div style="color: #10a37f; margin: 10px 0;">✓ ${point}</div>`).join('') || '<p>Analysis in progress...</p>'}
  </div>
  
  <div class="section">
    <h2>Issues - Problems to Fix</h2>
    ${scores.seo.issues?.map(issue => `<div class="issue">✗ ${issue}</div>`).join('') || '<p>No issues found</p>'}
  </div>
  
  <div class="section">
    <h2>Recommendations - Action Items</h2>
    ${scores.seo.recommendations?.map(rec => `<div class="recommendation">→ ${rec}</div>`).join('') || '<p>No recommendations</p>'}
  </div>
</body>
</html>
    `
    const blob = new Blob([html], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `content-audit-report-${Date.now()}.html`
    link.click()
    URL.revokeObjectURL(url)
  }

  const shareResults = async () => {
    const shareText = `Content Audit Score: ${results.overall_score.toFixed(1)}/100\\n\\nSEO: ${scores.seo.score}\\nSERP: ${scores.serp.score}\\nAEO: ${scores.aeo.score}\\nHumanization: ${scores.humanization.score}\\nDifferentiation: ${scores.differentiation.score}`
    
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Content Audit Results',
          text: shareText
        })
      } catch (err) {
        console.log('Share cancelled')
      }
    } else {
      navigator.clipboard.writeText(shareText)
      alert('Results copied to clipboard!')
    }
  }

  const API_URL = import.meta.env.VITE_API_URL || (import.meta.env.MODE === 'production' ? '/api' : 'http://localhost:5000/api')

  const handleAIRewrite = async (type, customPrompt = null) => {
    setAiImproving(true)
    try {
      const response = await fetch(`${API_URL}/improve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: results.original_text || '',
          improvement_type: type,
          target_keyword: scores.serp?.details?.target_keyword || '',
          analysis: scores,
          custom_prompt: customPrompt
        })
      })
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }
      
      const data = await response.json()
      setImprovedContent({ 
        type, 
        content: data,
        original: results.original_text,
        timestamp: Date.now()
      })
    } catch (err) {
      console.error('AI rewrite failed:', err)
      setImprovedContent({
        type,
        content: {
          success: false,
          error: err.message || 'Failed to connect to AI service. Check your OpenAI API key in backend/.env'
        }
      })
    }
    setAiImproving(false)
  }

  const ScoreCard = ({ title, data }) => {
    const [isExpanded, setIsExpanded] = useState(true)
    
    return (
      <div className="score-card">
        <div className="score-header" onClick={() => setIsExpanded(!isExpanded)}>
          <h3>{title}</h3>
          <div className="header-right">
            <div className="score-badge" style={{ backgroundColor: getScoreColor(data.score) }}>
              {data.score}/100
            </div>
            <button className="expand-btn">{isExpanded ? '▼' : '▶'}</button>
          </div>
        </div>
        
        {/* Visual Progress Bar */}
        <div className="score-progress-bar">
          <div 
            className="score-progress-fill" 
            style={{ 
              width: `${data.score}%`,
              backgroundColor: getScoreColor(data.score)
            }}
          >
            <span className="progress-label">{data.score}%</span>
          </div>
        </div>
        
        {isExpanded && (
          <div className="score-details">{title === "SERP Performance" && data.details?.target_keyword && (
          <div className="serp-header">
            <strong>Target Keyword:</strong> "{data.details.target_keyword}"
            {data.details?.serp_summary && (
              <div className="serp-analysis">
                <strong>Current SERP Analysis (Top 10):</strong>
                {data.details.serp_summary.map((line, i) => (
                  <div key={i} className="point">- {line}</div>
                ))}
              </div>
            )}
          </div>
        )}
        
        {/* Strengths Section */}
        {data.details?.good_points && data.details.good_points.length > 0 && (
          <div className="analysis-section">
            <h4 className="analysis-section-heading strengths-heading">
              <span className="heading-icon">✓</span>
              <span className="heading-text">Strengths</span>
              <span className="heading-count">({data.details.good_points.length})</span>
            </h4>
            <div className="good-points">
              {data.details.good_points.map((point, i) => (
                <div key={i} className="point good">✓ {point}</div>
              ))}
            </div>
          </div>
        )}
        
        {/* Issues Section */}
        {data.issues && data.issues.length > 0 && (
          <div className="analysis-section">
            <h4 className="analysis-section-heading issues-heading">
              <span className="heading-icon">!</span>
              <span className="heading-text">Issues</span>
              <span className="heading-count">({data.issues.length})</span>
            </h4>
            <div className="issues">
              {data.issues.map((issue, i) => (
                <div key={i} className="point issue">✗ {issue}</div>
              ))}
            </div>
          </div>
        )}
        
        {/* Show ranking prediction for SERP */}
        {title === "SERP Performance" && data.details?.ranking_prediction && (
          <div className="ranking-prediction">
            <div className="point issue">
              Predicted Performance: Page {data.details.ranking_prediction.current_page} (positions {data.details.ranking_prediction.current_position}-{data.details.ranking_prediction.current_position + 5})
            </div>
          </div>
        )}
        
        {/* Recommendations Section */}
        {data.recommendations && data.recommendations.length > 0 && (
          <div className="analysis-section">
            <h4 className="analysis-section-heading recommendations-heading">
              <span className="heading-icon">→</span>
              <span className="heading-text">Recommendations</span>
              <span className="heading-count">({data.recommendations.length})</span>
            </h4>
            <div className="recommendations">
              {data.recommendations.map((rec, i) => (
                <div key={i} className="point rec">→ {rec}</div>
              ))}
            </div>
          </div>
        )}
        
        {/* Show improvement potential for SERP */}
        {title === "SERP Performance" && data.details?.ranking_prediction?.with_improvements && (
          <div className="improvement-potential">
            <div className="point rec">
              → With improvements: Predicted Page {data.details.ranking_prediction.with_improvements.current_page} potential (positions {data.details.ranking_prediction.with_improvements.current_position}-{data.details.ranking_prediction.with_improvements.current_position + 3})
            </div>
          </div>
        )}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="results-dashboard">
      <div className="overall-score">
        <h2>Overall Content Quality</h2>
        <div className="big-score" style={{ color: getScoreColor(results.overall_score) }}>
          {results.overall_score.toFixed(1)}/100
        </div>
        <div className="score-grade">
          {results.overall_score >= 90 ? 'Excellent' : 
           results.overall_score >= 80 ? 'Great' :
           results.overall_score >= 70 ? 'Good' :
           results.overall_score >= 60 ? 'Needs Work' : 'Poor'}
        </div>
        
        {/* Export Actions */}
        <div className="export-actions">
          <button className="export-btn" onClick={exportAsJSON} title="Download as JSON">
            Export JSON
          </button>
          <button className="export-btn" onClick={exportAsHTML} title="Download as HTML Report">
            Export Report
          </button>
          <button className="export-btn" onClick={shareResults} title="Share results">
            Share
          </button>
        </div>
      </div>

      {/* Content Metrics Dashboard */}
      {scores.seo?.details?.content_metrics && (
        <div className="metrics-dashboard">
          <h3>
            Content Metrics 
            <Tooltip text="Key metrics about your content length and structure">
              <span className="info-icon">i</span>
            </Tooltip>
          </h3>
          <div className="metrics-grid">
            <Tooltip text="Total word count - aim for 800-2000 words for SEO">
              <div className="metric-card">
                <div className="metric-icon">W</div>
                <div className="metric-value">{scores.seo.details.content_metrics.word_count}</div>
                <div className="metric-label">Words</div>
              </div>
            </Tooltip>
            <Tooltip text="Average reading time based on 200 words/minute">
              <div className="metric-card">
                <div className="metric-icon">T</div>
                <div className="metric-value">{scores.seo.details.content_metrics.reading_time_minutes}</div>
                <div className="metric-label">Min Read</div>
              </div>
            </Tooltip>
            <Tooltip text="Number of paragraphs - helps with content structure">
              <div className="metric-card">
                <div className="metric-icon">P</div>
                <div className="metric-value">{scores.seo.details.content_metrics.paragraph_count}</div>
                <div className="metric-label">Paragraphs</div>
              </div>
            </Tooltip>
            <Tooltip text="Total character count including spaces">
              <div className="metric-card">
                <div className="metric-icon">C</div>
                <div className="metric-value">{scores.seo.details.content_metrics.character_count}</div>
                <div className="metric-label">Characters</div>
              </div>
            </Tooltip>
          </div>
        </div>
      )}

      {/* Performance Comparison */}
      <div className="benchmark-section">
        <h3>Performance vs Industry Standards</h3>
        <div className="benchmark-grid">
          <div className="benchmark-item">
            <div className="benchmark-label">SEO Optimization</div>
            <div className="benchmark-bar-container">
              <div className="benchmark-average-marker" style={{left: '70%'}}>
                <span>Avg</span>
              </div>
              <div className="benchmark-bar" style={{width: `${scores.seo.score}%`, backgroundColor: getScoreColor(scores.seo.score)}}>
                <span className="benchmark-value">{scores.seo.score}%</span>
              </div>
            </div>
            <div className="benchmark-insight">
              {scores.seo.score >= 70 ? 'Above average' : 'Below average - needs improvement'}
            </div>
          </div>

          <div className="benchmark-item">
            <div className="benchmark-label">Content Humanization</div>
            <div className="benchmark-bar-container">
              <div className="benchmark-average-marker" style={{left: '65%'}}>
                <span>Avg</span>
              </div>
              <div className="benchmark-bar" style={{width: `${scores.humanization.score}%`, backgroundColor: getScoreColor(scores.humanization.score)}}>
                <span className="benchmark-value">{scores.humanization.score}%</span>
              </div>
            </div>
            <div className="benchmark-insight">
              {scores.humanization.score >= 65 ? 'Sounds natural' : 'May sound AI-generated'}
            </div>
          </div>

          <div className="benchmark-item">
            <div className="benchmark-label">Uniqueness Score</div>
            <div className="benchmark-bar-container">
              <div className="benchmark-average-marker" style={{left: '60%'}}>
                <span>Avg</span>
              </div>
              <div className="benchmark-bar" style={{width: `${scores.differentiation.score}%`, backgroundColor: getScoreColor(scores.differentiation.score)}}>
                <span className="benchmark-value">{scores.differentiation.score}%</span>
              </div>
            </div>
            <div className="benchmark-insight">
              {scores.differentiation.score >= 60 ? 'Stands out from competition' : 'Too generic'}
            </div>
          </div>
        </div>
      </div>

      {/* AI Rewrite Tool - Enhanced */}
      <div className="ai-rewrite-tool">
        <div className="tool-header">
          <div className="tool-title">
            <h3>AI Content Rewriter</h3>
            <p className="tool-subtitle">Transform your content with AI-powered improvements</p>
          </div>
        </div>

        {/* Rewrite Mode Selection */}
        <div className="rewrite-modes">
          <h4>Select Rewrite Mode:</h4>
          <div className="mode-grid">
            <button 
              className={`mode-btn ${improvedContent?.type === 'full' ? 'active' : ''}`}
              onClick={() => handleAIRewrite('full')}
              disabled={aiImproving}
              title="Complete content rewrite addressing all issues"
            >
              <span className="mode-icon">*</span>
              <span className="mode-name">Full Rewrite</span>
              <span className="mode-desc">Fix all issues</span>
            </button>
            
            <button 
              className={`mode-btn ${improvedContent?.type === 'seo' ? 'active' : ''}`}
              onClick={() => handleAIRewrite('seo')}
              disabled={aiImproving}
              title="Optimize for search engines and keywords"
            >
              <span className="mode-icon">⊕</span>
              <span className="mode-name">SEO Optimize</span>
              <span className="mode-desc">Better keywords</span>
            </button>
            
            <button 
              className={`mode-btn ${improvedContent?.type === 'humanize' ? 'active' : ''}`}
              onClick={() => handleAIRewrite('humanize')}
              disabled={aiImproving}
              title="Make content sound more natural and human"
            >
              <span className="mode-icon">H</span>
              <span className="mode-name">Humanize</span>
              <span className="mode-desc">Natural tone</span>
            </button>
            
            <button 
              className={`mode-btn ${improvedContent?.type === 'readability' ? 'active' : ''}`}
              onClick={() => handleAIRewrite('readability')}
              disabled={aiImproving}
              title="Simplify language and improve clarity"
            >
              <span className="mode-icon">R</span>
              <span className="mode-name">Readability</span>
              <span className="mode-desc">Easier to read</span>
            </button>
            
            <button 
              className={`mode-btn ${improvedContent?.type === 'engagement' ? 'active' : ''}`}
              onClick={() => handleAIRewrite('engagement')}
              disabled={aiImproving}
              title="Make content more engaging and compelling"
            >
              <span className="mode-icon">E</span>
              <span className="mode-name">Engagement</span>
              <span className="mode-desc">More engaging</span>
            </button>
            
            <button 
              className={`mode-btn ${improvedContent?.type === 'meta' ? 'active' : ''}`}
              onClick={() => handleAIRewrite('meta')}
              disabled={aiImproving}
              title="Generate optimized meta description"
            >
              <span className="mode-icon">M</span>
              <span className="mode-name">Meta Description</span>
              <span className="mode-desc">Perfect meta</span>
            </button>
          </div>
        </div>

        {/* Loading State */}
        {aiImproving && (
          <div className="ai-loading-state">
            <div className="loading-spinner"></div>
            <p>AI is analyzing and rewriting your content...</p>
            <div className="loading-bar">
              <div className="loading-progress"></div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {improvedContent && improvedContent.content && (
          <div className="ai-result-container">
            {improvedContent.content.error ? (
              <div className="error-panel">
                <div className="error-icon">!</div>
                <h4>Error Occurred</h4>
                <p>{improvedContent.content.error}</p>
                <button 
                  className="retry-btn"
                  onClick={() => handleAIRewrite(improvedContent.type)}
                >
                  Retry
                </button>
              </div>
            ) : (
              <>
                {/* Success Header */}
                <div className="result-header">
                  <div className="result-title">
                    <span className="success-icon">✓</span>
                    <h4>AI Rewrite Complete</h4>
                    <span className="mode-badge">{improvedContent.type}</span>
                  </div>
                  <div className="result-actions">
                    <button 
                      className="action-icon-btn"
                      onClick={() => handleAIRewrite(improvedContent.type)}
                      title="Regenerate with different variation"
                    >
                      Regenerate
                    </button>
                    <button 
                      className="action-icon-btn"
                      onClick={() => {
                        const content = improvedContent.content.improved_content || improvedContent.content.improved_meta || improvedContent.content.improved_paragraph || ''
                        navigator.clipboard.writeText(content)
                        setCopyButtonText('Copied!')
                        setTimeout(() => setCopyButtonText('Copy'), 2000)
                      }}
                      title="Copy to clipboard"
                    >
                      {copyButtonText || 'Copy'}
                    </button>
                  </div>
                </div>

                {/* Side-by-Side Comparison */}
                {improvedContent.content.improved_content && (
                  <div className="comparison-view">
                    <div className="comparison-column original-column">
                      <div className="column-header">
                        <h5>Original Content</h5>
                        <span className="word-count">{improvedContent.original?.split(' ').length || 0} words</span>
                      </div>
                      <div className="content-box original-content">
                        {improvedContent.original || 'No original content'}
                      </div>
                    </div>
                    
                    <div className="comparison-divider">
                      <div className="divider-icon">→</div>
                    </div>
                    
                    <div className="comparison-column improved-column">
                      <div className="column-header">
                        <h5>Improved Content</h5>
                        <span className="word-count">{improvedContent.content.improved_content.split(' ').length || 0} words</span>
                      </div>
                      <div className="content-box improved-content">
                        {improvedContent.content.improved_content}
                      </div>
                    </div>
                  </div>
                )}

                {/* Meta Description Result */}
                {improvedContent.content.improved_meta && (
                  <div className="meta-result">
                    <div className="meta-preview">
                      <h5>Generated Meta Description</h5>
                      <div className="meta-box">
                        {improvedContent.content.improved_meta}
                      </div>
                      <div className="meta-stats">
                        <span className={improvedContent.content.improved_meta.length >= 150 && improvedContent.content.improved_meta.length <= 160 ? 'stat-good' : 'stat-warning'}>
                          {improvedContent.content.improved_meta.length} characters
                          {improvedContent.content.improved_meta.length >= 150 && improvedContent.content.improved_meta.length <= 160 ? ' Perfect length' : ' Should be 150-160'}
                        </span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Changes Summary */}
                {improvedContent.content.changes_made && (
                  <div className="changes-summary">
                    <h5>Changes Made:</h5>
                    <ul>
                      {improvedContent.content.changes_made.map((change, i) => (
                        <li key={i}>✓ {change}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Quick Actions */}
                <div className="quick-actions">
                  <button 
                    className="action-btn secondary"
                    onClick={() => setImprovedContent(null)}
                  >
                    Close
                  </button>
                  <button 
                    className="action-btn primary"
                    onClick={() => {
                      const content = improvedContent.content.improved_content || improvedContent.content.improved_meta || ''
                      navigator.clipboard.writeText(content)
                      alert('Content copied! You can now paste it into your editor.')
                    }}
                  >
                    Copy & Use Content
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </div>

      {/* Enhanced AI Rank Simulator - Signature Feature */}
      {scores.serp?.details?.ranking_prediction && (
        <div className="rank-simulator-enhanced">
          <h3>AI Predictive Rank Simulator</h3>
          <p className="simulator-subtitle">See exactly how your content will rank after fixes</p>
          
          <div className="rank-jump-visualization">
            <div className="rank-position current-rank">
              <div className="rank-label">Current Position</div>
              <div className="rank-number">#{scores.serp.details.ranking_prediction.current_position}</div>
              <div className="rank-page">Page {scores.serp.details.ranking_prediction.current_page}</div>
            </div>
            
            <div className="rank-arrow-container">
              <div className="rank-improvement">
                +{scores.serp.details.ranking_prediction.current_position - 
                  (scores.serp.details.ranking_prediction.with_improvements?.current_position || scores.serp.details.ranking_prediction.current_position)} positions
              </div>
              <div className="rank-arrow">→</div>
            </div>
            
            <div className="rank-position improved-rank">
              <div className="rank-label">After Improvements</div>
              <div className="rank-number predicted">
                #{scores.serp.details.ranking_prediction.with_improvements?.current_position || scores.serp.details.ranking_prediction.current_position}
              </div>
              <div className="rank-page">Page {scores.serp.details.ranking_prediction.with_improvements?.current_page || scores.serp.details.ranking_prediction.current_page}</div>
            </div>
          </div>
          
          <div className="rank-progress-bar">
            <div 
              className="rank-progress-fill"
              style={{ 
                width: `${((scores.serp.details.ranking_prediction.current_position - 
                  (scores.serp.details.ranking_prediction.with_improvements?.current_position || scores.serp.details.ranking_prediction.current_position)) / 
                  scores.serp.details.ranking_prediction.current_position) * 100}%` 
              }}
            />
          </div>
          <p className="rank-impact">
            {scores.serp.details.ranking_prediction.with_improvements?.current_position <= 10 
              ? 'Page 1 Potential!' 
              : scores.serp.details.ranking_prediction.with_improvements?.current_position <= 20
              ? 'Top 20 Achievable'
              : 'Significant Improvement Possible'}
          </p>
        </div>
      )}

      {/* Competitor Fingerprint - Another Signature Feature */}
      {scores.serp?.details?.serp_data?.patterns && (
        <div className="competitor-fingerprint">
          <h3>Competitor Intelligence Map</h3>
          <p className="fingerprint-subtitle">What top 10 SERP leaders are doing</p>
          
          <div className="fingerprint-grid">
            <div className="fingerprint-card">
              <div className="fingerprint-icon">D</div>
              <div className="fingerprint-stat">{scores.serp.details.serp_data.patterns.has_stats}%</div>
              <div className="fingerprint-label">Include Data/Stats</div>
            </div>
            
            <div className="fingerprint-card">
              <div className="fingerprint-icon">B</div>
              <div className="fingerprint-stat">{scores.serp.details.serp_data.patterns.has_examples}%</div>
              <div className="fingerprint-label">Use Case Studies</div>
            </div>
            
            <div className="fingerprint-card">
              <div className="fingerprint-icon">=</div>
              <div className="fingerprint-stat">{scores.serp.details.serp_data.patterns.has_comparisons}%</div>
              <div className="fingerprint-label">Have Comparisons</div>
            </div>
            
            <div className="fingerprint-card">
              <div className="fingerprint-icon">L</div>
              <div className="fingerprint-stat">{scores.serp.details.serp_data.patterns.has_lists}%</div>
              <div className="fingerprint-label">Use Lists/Bullets</div>
            </div>
          </div>
          
          <div className="fingerprint-insight">
            <strong>Key Insight:</strong> Top rankers average {scores.serp.details.serp_data.patterns.avg_stats || 6} data points per article
          </div>
        </div>
      )}

      {results.rank_prediction && (
        <div className="rank-simulator">
          <h3>AI Rank Prediction</h3>
          <div className="rank-comparison">
            <div className="rank-box current">
              <span>Current Estimate</span>
              <strong>Rank #{results.rank_prediction.current_estimated_rank}</strong>
            </div>
            <div className="arrow">→</div>
            <div className="rank-box improved">
              <span>With Improvements</span>
              <strong>Rank #{results.rank_prediction.improved_estimated_rank}</strong>
            </div>
          </div>
          <p className="rank-message">{results.rank_prediction.message}</p>
        </div>
      )}

      <div className="scores-grid">
        <ScoreCard title="SEO Score" data={scores.seo} />
        <ScoreCard title="SERP Performance" data={scores.serp} />
        <ScoreCard title="AEO Score" data={scores.aeo} />
        <ScoreCard title="Humanization" data={scores.humanization} />
        <ScoreCard title="Differentiation" data={scores.differentiation} />
      </div>

      {scores.humanization.details?.heatmap && (
        <div className="heatmap-section">
          <h3>Humanization Heatmap</h3>
          <p>Red = AI-like patterns | Green = Human-like</p>
          {scores.humanization.details.heatmap.slice(0, 5).map((item, i) => (
            <div 
              key={i} 
              className={`heatmap-item ${item.score > 50 ? 'ai-like' : 'human-like'}`}
            >
              <span className="heatmap-score">{item.score}</span>
              <span className="heatmap-text">{item.sentence}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
