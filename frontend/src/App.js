import './App.css';
import React from 'react';
import Table from './components/Table';
import Add from './components/Add';
import { useState, useEffect } from 'react';
import { getAllUrls } from './ApiFunctions';

function App() {
  const [urlData, setUrlData] = useState([]);

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


  return (
    <div className="App">
      <Table urlData={urlData} onDeleteAlias={onDeleteAlias} />
      <Add onAddUrl={onAddUrl} />
    </div>
  );
}

export default App;
