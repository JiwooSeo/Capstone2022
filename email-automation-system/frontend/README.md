# Email Automation & Scheduling System - Frontend

Next.js React frontend for email automation dashboard with Google OAuth integration.

## Features

- Google OAuth login integration
- Interactive dashboard with statistics
- Calendar view for scheduled events
- Settings page for account management
- Responsive design with TailwindCSS

## Setup

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
npm install
```

### Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

- `pages/` - Next.js pages
  - `index.tsx` - Login/home page
  - `dashboard.tsx` - Main dashboard
  - `calendar.tsx` - Event calendar
  - `settings.tsx` - User settings
- `components/` - React components (placeholder)
- `lib/` - Utilities and API client (placeholder)
- `styles/` - Global styles
- `public/` - Static files

## Authentication

OAuth flow:
1. User clicks "Sign in with Google"
2. Redirects to backend `/api/auth/google-callback`
3. Backend returns JWT token
4. Token stored in localStorage
5. Token sent in Authorization header for API calls

## API Integration

API calls use the `NEXT_PUBLIC_API_URL` environment variable:

```typescript
const token = localStorage.getItem('access_token')
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/events`, {
  headers: {
    Authorization: `Bearer ${token}`,
  },
})
```

## Pages

### Home (/)
Login page with Google OAuth button for unauthenticated users.
Shows dashboard overview for authenticated users.

### Dashboard (/dashboard)
- Overview statistics
- Total events count
- Breakdown by event type
- Email count

### Calendar (/calendar)
- List of upcoming events
- Sorted by date and time
- Color-coded by event type
- Links to edit events

### Settings (/settings)
- User profile information
- Gmail account management
- Logout button
- Access revocation

## Technologies

- **Next.js** - React framework
- **React Query** - Server state management
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Zustand** - Client state (optional)

## Development Tips

- API documentation: http://localhost:8000/docs
- Browser DevTools for debugging
- Next.js dev tools for component inspection

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

```bash
docker build -t email-automation-frontend .
docker run -p 3000:3000 email-automation-frontend
```

### Manual

```bash
npm run build
npm start
```

## Troubleshooting

### CORS Issues
Ensure backend CORS is configured for frontend origin.

### API Connection Issues
Check `NEXT_PUBLIC_API_URL` environment variable.

### OAuth Login Not Working
- Verify Google OAuth credentials
- Check redirect URI in Google Cloud Console
- Ensure backend is running

## Contributing

Follow the project structure and use TypeScript for type safety.
