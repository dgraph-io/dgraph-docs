import React, { ReactNode } from 'react';
import CodeBlock from '@theme/CodeBlock';
import styles from './styles.module.css';

interface HighlightProps {
  language?: string;
  linenos?: string | boolean;
  hl_lines?: string;
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
      // Handle template literals (backtick strings)
      if (child.type === 'code' && child.props && typeof child.props.children === 'string') {
        code += child.props.children;
      } else if (child.props && child.props.children) {
        code += extractCodeFromChildren(child.props.children);
      } else if (child.props && child.props.className && child.props.className.includes('language-')) {
        code += extractCodeFromChildren(child.props.children);
      }
    }
  });
  
  return code.trim();
}

// Parse hl_lines parameter (e.g., "7" or "6-7" or "7,9,11")
function parseHighlightLines(hlLines?: string): number[] {
  if (!hlLines) return [];
  
  const lines: number[] = [];
  const parts = hlLines.split(',');
  
  for (const part of parts) {
    const trimmed = part.trim();
    if (trimmed.includes('-')) {
      // Range like "6-7"
      const [start, end] = trimmed.split('-').map(Number);
      for (let i = start; i <= end; i++) {
        lines.push(i);
      }
    } else {
      // Single line number
      const lineNum = Number(trimmed);
      if (!isNaN(lineNum)) {
        lines.push(lineNum);
      }
    }
  }
  
  return lines;
}

export default function Highlight({ 
  language = 'text', 
  linenos = false, 
  hl_lines,
  children 
}: HighlightProps) {
  const codeContent = extractCodeFromChildren(children);
  const highlightLines = parseHighlightLines(hl_lines);
  
  // Docusaurus CodeBlock supports highlighting via the `highlight` prop
  // It expects a string like "1,3,5" or ranges like "1-3,5"
  // Convert array of line numbers to string format
  let highlightString: string | undefined = undefined;
  if (highlightLines.length > 0) {
    // Group consecutive lines into ranges
    const ranges: string[] = [];
    let rangeStart = highlightLines[0];
    let rangeEnd = highlightLines[0];
    
    for (let i = 1; i < highlightLines.length; i++) {
      if (highlightLines[i] === rangeEnd + 1) {
        rangeEnd = highlightLines[i];
      } else {
        if (rangeStart === rangeEnd) {
          ranges.push(rangeStart.toString());
        } else {
          ranges.push(`${rangeStart}-${rangeEnd}`);
        }
        rangeStart = highlightLines[i];
        rangeEnd = highlightLines[i];
      }
    }
    
    // Add the last range
    if (rangeStart === rangeEnd) {
      ranges.push(rangeStart.toString());
    } else {
      ranges.push(`${rangeStart}-${rangeEnd}`);
    }
    
    highlightString = ranges.join(',');
  }

  return (
    <div className={styles.highlight}>
      <CodeBlock 
        language={language}
        showLineNumbers={linenos === true || linenos === 'true'}
        {...(highlightString && { highlight: highlightString })}
      >
        {codeContent}
      </CodeBlock>
    </div>
  );
}

