
export default function Fallback({ error, resetErrorBoundary }: { error: string, resetErrorBoundary: () => void }) {
    return (
        <div role="alert">
            <p>Something went wrong:</p>
            <pre style={{ color: "red" }}>{error}</pre>
            <button
                onClick={resetErrorBoundary}
            >Try again</button>
        </div>
    );
}
