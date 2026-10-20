import {useState} from 'react';

const App = () => {
    const [text, setText] = useState("");
    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [analyses, setAnalyses] = useState([]);
    const [error, setError] = useState("");

    const handleSubmit = async (e, isUrlRequest) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setAnalyses([]);
        
        try {
            let response;
            if (isUrlRequest) {
                response = await fetch('http://127.0.0.1:8000/analyze-url', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({'url': url})
                })
            }
            else {
                response = await fetch('http://127.0.0.1:8000/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({'text': text})
                })
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Request failed");
            }

            const result = await response.json();
            setAnalyses(result.analyses);

        } catch (error) {
            setError(error.message);

        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <h1>Chinese Reader</h1>

            <form onSubmit={(e) => handleSubmit(e, true)}>
                <input type="url" placeholder="Enter the url of the chapter to analyze" value={url} onChange={(e) => {setUrl(e.target.value)}}/>
                <button disabled={loading} type="submit"> {loading ? "Analyzing..." : "Analyze"} </button>
            </form>

            <form onSubmit={(e) => handleSubmit(e, false)}>
                <textarea rows="5" placeholder="Enter the text to analyze" value={text} onChange={(e) => {setText(e.target.value)}} ></textarea>
                <button disabled={loading} type="submit"> {loading ? "Analyzing..." : "Analyze"} </button>
            </form>
            
            {error.length !== 0 && (
                <div>
                    <h2>Error:</h2>
                    <p>{error}</p>
                </div>
            )}

            <h2>Analyses:</h2>
            <ul>
                {analyses.map((analysis, index) => (
                    <li key={index}>
                        <h3>{analysis.sentence}</h3>
                        <p>HSK {analysis.hsk_level}</p>
                        <p>Pattern: {analysis.pattern}</p>
                        <p>{analysis.explanation}</p>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default App;