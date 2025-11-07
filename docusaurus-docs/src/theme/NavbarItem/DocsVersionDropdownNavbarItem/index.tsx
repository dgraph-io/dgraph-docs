import React, {useMemo} from 'react';
import {useLocation} from '@docusaurus/router';
import DocsVersionDropdownNavbarItemType from '@theme-original/NavbarItem/DocsVersionDropdownNavbarItem';
import type {Props} from '@theme/NavbarItem/DocsVersionDropdownNavbarItem';

/**
 * A context-aware version dropdown that automatically detects which plugin
 * the current page belongs to based on the URL path.
 * 
 * This is a swizzled version of DocsVersionDropdownNavbarItem that detects
 * the plugin ID from the current URL path instead of using a hardcoded value.
 */
export default function DocsVersionDropdownNavbarItem(
  props: Props,
): JSX.Element {
  const location = useLocation();
  
  // Detect which plugin the current page belongs to based on the path
  const detectedPluginId = useMemo(() => {
    const pathname = location.pathname;
    
    // Check for GraphQL pages (handles both /graphql/... and /graphql/v24.1/... patterns)
    if (pathname.startsWith('/graphql')) {
      return 'graphql';
    }
    
    // Check for Ratel pages
    if (pathname.startsWith('/ratel')) {
      return 'ratel';
    }
    
    // Check for Learn/Tutorials pages
    if (pathname.startsWith('/learn')) {
      return 'learn';
    }
    
    // Check if path starts with a version prefix (e.g., /v24.1/...)
    // This would be for the 'docs' plugin which has routeBasePath: ''
    const versionMatch = pathname.match(/^\/v[\d.]+/);
    if (versionMatch) {
      // If there's a version prefix, check what comes after
      const afterVersion = pathname.substring(versionMatch[0].length);
      if (afterVersion.startsWith('/graphql')) {
        return 'graphql';
      }
      if (afterVersion.startsWith('/ratel')) {
        return 'ratel';
      }
      if (afterVersion.startsWith('/learn')) {
        return 'learn';
      }
      // If version prefix exists but no plugin path, it's the docs plugin
      return 'docs';
    }
    
    // Default to 'docs' for root and other paths
    return 'docs';
  }, [location.pathname]);

  // Use the detected plugin ID, but allow override from props if provided
  const finalPluginId = props.docsPluginId || detectedPluginId;

  return <DocsVersionDropdownNavbarItemType {...props} docsPluginId={finalPluginId} />;
}

