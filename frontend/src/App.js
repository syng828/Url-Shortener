import './App.css';
import React from 'react';
import Table from './components/Table';
import Add from './components/Add';
import ErrorComponent from './components/ErrorComponent';
import { useState, useEffect } from 'react';
import { getAllUrls } from './ApiFunctions';

function App() {
  const [urlData, setUrlData] = useState([]);
  const [errorToggle, setErrorToggle] = useState(true);
  const [errorDetails, setErrorDetails] = useState(null);
  const [addOpen, setAddOpen] = useState(false);


  useEffect(() => {
    async function getInfo() {
      const urlsFromDB = await getAllUrls();
      if (!urlsFromDB.error) {
        console.log(urlsFromDB.responseData);
        setUrlData(urlsFromDB.responseData.url_list)
      }
    }
    getInfo();
  }, [])

  const onAddUrl = async (newData) => {
    const updatedData = [...urlData, newData];
    setUrlData(updatedData);
  }

  const onDeleteAlias = async (aliasToDelete) => {
    const updatedData = urlData.filter(entry => entry.alias !== aliasToDelete);
    setUrlData(updatedData);
  }

  const handleToggle = () => {
    setErrorToggle(!errorToggle);
  };

  const onError = (errors) => {
    setErrorDetails(errors);
    setTimeout(() => {
      setErrorDetails(null);
    }, 3000);
  }


  return (
    <div className="App">
      <h1>Url Shortener</h1>
      <div className="row-wrapper">
        <Table urlData={urlData} onDeleteAlias={onDeleteAlias} errorToggle={errorToggle} onError={onError} />
        <div className="col-wrapper">
          <button className="btn" onClick={() => setAddOpen(true)}>Add</button>
          <label className="errorCheck">
            <input
              type="checkbox"
              checked={errorToggle}
              onChange={handleToggle}
            />
            Display Error
          </label>
        </div>
      </div>
      {addOpen && <Add closeAdd={() => { setAddOpen(false); }} onAddUrl={onAddUrl} errorToggle={errorToggle} onError={onError} />}
      {errorDetails && <ErrorComponent closeError={() => setErrorDetails(null)} message={errorDetails} />}
    </div>
  );
}

export default App;
