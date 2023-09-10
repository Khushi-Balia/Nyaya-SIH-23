import React from "react";
import HeroSection from "./components/HeroSection";

const Home = () => {
  const data = {
    name: "Nyaya: Law Simplified",
  };

  return <HeroSection myData={data} />;
};

export default Home;