# Deployment Guide for Runnable Component

The `Runnable` component allows users to execute DQL queries directly from the documentation. This guide explains how to configure it for deployment on Cloudflare Pages (or other hosting platforms).

## Configuration

The Dgraph endpoint is configured via the `DGRAPH_ENDPOINT` environment variable, which is set at build time and stored in `docusaurus.config.ts`.

### Local Development

By default, the component uses `http://localhost:8080` for local development. No configuration needed - just start your local Dgraph instance.

### Production Deployment

For production deployment, you need to:

1. **Set up a publicly accessible Dgraph instance** (or use a proxy)
2. **Configure the endpoint** via environment variable at build time

## Deployment Options

### Option 1: Public Dgraph Instance (Recommended for Demo/Testing)

If you have a publicly accessible Dgraph instance:

1. **Set the environment variable during build:**
   ```bash
   DGRAPH_ENDPOINT=https://your-dgraph-instance.com docusaurus build
   ```

2. **For Cloudflare Pages:**
   - Go to your Cloudflare Pages project settings
   - Navigate to "Environment variables"
   - Add: `DGRAPH_ENDPOINT` = `https://your-dgraph-instance.com`
   - This will be available during the build process

### Option 2: Cloudflare Worker/Function as Proxy

For better security and control, use a Cloudflare Worker to proxy requests:

1. **Create a Cloudflare Worker** (`functions/dgraph-proxy.ts` or similar):
   ```typescript
   export async function onRequestPost(context: EventContext): Promise<Response> {
     const request = context.request;
     const body = await request.text();
     
     // Forward to your Dgraph instance (can be private/internal)
     const response = await fetch('https://your-internal-dgraph.com/query', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/dql',
       },
       body: body,
     });
     
     return response;
   }
   ```

2. **Update the Runnable component** to use the proxy endpoint:
   ```bash
   DGRAPH_ENDPOINT=/dgraph-proxy
   ```

### Option 3: Disable in Production

If you don't want the Runnable component to work in production:

1. Set `DGRAPH_ENDPOINT` to an empty string or invalid URL
2. The component will show the "host unavailable" message

## Security Considerations

⚠️ **Important Security Notes:**

1. **CORS Configuration**: Your Dgraph instance must allow CORS requests from your documentation domain:
   ```bash
   # In your Dgraph configuration
   --cors "origin=https://docs.dgraph.io,https://your-docs-domain.com"
   ```

2. **Rate Limiting**: Consider implementing rate limiting on your Dgraph endpoint to prevent abuse.

3. **Authentication**: If your Dgraph instance requires authentication, you'll need to:
   - Use a proxy (Option 2) to add authentication headers server-side
   - Or implement client-side authentication (not recommended for public docs)

4. **Read-Only Access**: For public documentation, consider:
   - Using a read-only Dgraph instance
   - Or restricting mutations via Dgraph ACL

## Cloudflare Pages Setup

1. **Build Settings:**
   - Build command: `cd docusaurus-docs && npm run build`
   - Build output directory: `docusaurus-docs/build`
   - Root directory: `/`

2. **Environment Variables:**
   - Add `DGRAPH_ENDPOINT` in Cloudflare Pages dashboard
   - Value: Your public Dgraph endpoint URL (e.g., `https://play.dgraph.io`)

3. **Build Environment:**
   - The environment variable will be available during build time
   - It gets baked into the static site configuration

## Testing

After deployment:

1. Visit your deployed documentation
2. Find a page with a `<Runnable>` component
3. Click "Run Query" - it should connect to your configured endpoint
4. If the endpoint is unavailable, you'll see: "Start a local Dgraph cluster populated with the movies data..."

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console:
- Ensure your Dgraph instance allows requests from your documentation domain
- Check Dgraph's `--cors` flag configuration

### Network Errors

If queries fail with network errors:
- Verify the `DGRAPH_ENDPOINT` is correctly set
- Check that the endpoint is publicly accessible
- Ensure the endpoint URL doesn't have a trailing slash (the component adds `/query`)

### Build-Time vs Runtime

Note: The endpoint is configured at **build time**, not runtime. To change it:
1. Update the environment variable
2. Rebuild and redeploy

