interface PageOneProps {
  onBack: () => void;
}

function PageOne({ onBack }: PageOneProps) {
  return (
    <div>
      <h1>Coming soon...</h1>
      <button onClick={onBack}>Back to Home</button>
    </div>
  );
}

export default PageOne;