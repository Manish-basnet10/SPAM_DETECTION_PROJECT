import React, { useState } from "react";
import SpamForm from "../components/SpamForm";
import Result from "../components/Result";

function Home() {
  const [result, setResult] = useState("");

  return (
    <div className="container">
      <SpamForm setResult={setResult} />
      <Result result={result} />
    </div>
  );
}

export default Home;
