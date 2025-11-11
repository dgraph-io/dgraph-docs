import React, { ReactNode, useState } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import CodeBlock from '@theme/CodeBlock';
import styles from './styles.module.css';

interface RunnableProps {
  children: ReactNode;
}

// Helper function to extract code from MDX children
function extractCodeFromChildren(children: ReactNode): string {
  if (typeof children === 'string') {
    return children.trim();
  }

  let code = '';
  
  React.Children.forEach(children, (child) => {
    if (typeof child === 'string') {
      code += child;
    } else if (React.isValidElement(child)) {
      const props = child.props as { children?: ReactNode; className?: string };
      // Check if it's a code element or has code in props
      if (props?.children) {
        code += extractCodeFromChildren(props.children);
      } else if (props?.className && props.className.includes('language-')) {
        // It's a code element with language class
        if (props.children) {
          code += extractCodeFromChildren(props.children);
        }
      }
    }
  });
  
  return code.trim();
}

export default function Runnable({ children }: RunnableProps) {
  // Get Dgraph endpoint from config
  const { siteConfig } = useDocusaurusContext();
  const dgraphEndpoint = (siteConfig.customFields?.dgraphEndpoint as string) || 'http://localhost:8080';
  
  // Extract code content from children
  const initialCodeContent = extractCodeFromChildren(children);
  
  // State for query execution
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [hostUnavailable, setHostUnavailable] = useState(false);
  
  // State for editing
  const [isEditing, setIsEditing] = useState(false);
  const [codeContent, setCodeContent] = useState(initialCodeContent);

  // Check if query has been modified
  const isModified = codeContent !== initialCodeContent;

  // Toggle edit mode
  const toggleEdit = () => {
    setIsEditing(!isEditing);
  };

  // Reset query to original
  const resetQuery = () => {
    setCodeContent(initialCodeContent);
    setIsEditing(false);
  };

  // Clear result
  const clearResult = () => {
    setResult(null);
    setError(null);
    setHostUnavailable(false);
  };

  // Execute the query
  const executeQuery = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    setHostUnavailable(false);
    setIsEditing(false); // Exit edit mode when running

    try {
      const response = await fetch(`${dgraphEndpoint}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/dql',
        },
        body: codeContent,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      // Check if it's a network error (host unavailable)
      // Network errors typically throw TypeError with messages like:
      // - "Failed to fetch"
      // - "NetworkError when attempting to fetch resource"
      // - "fetch failed"
      const errorMessage = err instanceof Error ? err.message : String(err);
      const isNetworkError = 
        err instanceof TypeError && 
        (errorMessage.includes('fetch') || 
         errorMessage.includes('Failed to fetch') || 
         errorMessage.includes('NetworkError') ||
         errorMessage.includes('network'));
      
      if (isNetworkError) {
        setHostUnavailable(true);
      } else {
        setError(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.runnable}>
      <div className={styles.runnableContainer}>
        <div className={styles.queryPanel}>
          <div className={styles.queryHeader}>
            <span className={styles.queryLabel}>Query</span>
            <div className={styles.queryActions}>
              {isModified && (
                <button
                  className={styles.iconButton}
                  onClick={resetQuery}
                  title="Reset to original query"
                  disabled={loading}
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 16 16"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1.333 8C1.333 4.318 4.318 1.333 8 1.333c2.182 0 4.091 1.182 5.091 2.909M14.667 8c0 3.682-2.985 6.667-6.667 6.667-2.182 0-4.091-1.182-5.091-2.909M1.333 8h4M14.667 8h-4M8 1.333v4M8 14.667v-4"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </button>
              )}
              <button
                className={styles.iconButton}
                onClick={toggleEdit}
                title={isEditing ? "Cancel editing" : "Edit query"}
                disabled={loading}
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  {isEditing ? (
                    <path
                      d="M2 2L14 14M14 2L2 14"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  ) : (
                    <path
                      d="M11.333 2.667a2.828 2.828 0 0 1 4 4L5.333 15.333l-4 1.334 1.334-4L11.333 2.667z"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      fill="none"
                    />
                  )}
                </svg>
              </button>
              <button
                className={styles.runButton}
                onClick={executeQuery}
                disabled={loading}
              >
                {loading ? 'Running...' : 'Run Query'}
              </button>
            </div>
          </div>
          {isEditing ? (
            <textarea
              className={styles.queryEditor}
              value={codeContent}
              onChange={(e) => setCodeContent(e.target.value)}
              spellCheck={false}
            />
          ) : (
            <CodeBlock language="dql">{codeContent}</CodeBlock>
          )}
        </div>
        <div className={styles.resultPanel}>
          <div className={styles.resultHeader}>
            <span className={styles.resultLabel}>Result</span>
            {(result || error || hostUnavailable) && (
              <button
                className={styles.iconButton}
                onClick={clearResult}
                title="Clear result"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12 4L4 12M4 4L12 12"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                </svg>
              </button>
            )}
          </div>
          <div className={styles.resultContent}>
            {loading && (
              <div className={styles.loading}>Executing query...</div>
            )}
            {hostUnavailable && !loading && (
              <div className={styles.hostUnavailable}>
                Start a local Dgraph cluster populated with the movies data...
              </div>
            )}
            {error && !hostUnavailable && (
              <div className={styles.error}>
                <strong>Error:</strong>
                <pre>{error}</pre>
              </div>
            )}
            {result && !loading && (
              <CodeBlock language="json">{result}</CodeBlock>
            )}
            {!result && !loading && !error && !hostUnavailable && (
              <div className={styles.placeholder}>
                Click "Run Query" to execute the query and see results here.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

