import { ErrorBoundary } from 'react-error-boundary'
import Fallback from "./components/Error/ErrorFallback"
import { RouterProvider } from 'react-router-dom'
import Router from './providers/Router'
export default function App() {

  return (
    <ErrorBoundary
      FallbackComponent={Fallback}>
      <RouterProvider router={Router} />
    </ErrorBoundary>
  )
}

