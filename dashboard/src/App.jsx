import React, { useState } from "react";
import axios from "axios";
import './App.css'
import Chart from './componenets/chart'
import MyTable from './componenets/table'

function App() {
  const [historicaldata, setHistoricalData] = useState([]);
  const [balance, setBalancelData] = useState([]);
  const [orderingdata, setOrderingData] = useState([]);

  const formdata = {
    "granularity": 300,
  }

  React.useEffect(() => {
    const interval = setInterval(() => {
      axios
        .post("http://34.135.119.144:5000/api/post", formdata)
        .then((res) => {
          console.log(res);
          console.log(res.data);
          setHistoricalData(res.data.historical_data);
          setBalancelData(res.data.balance);
          res.data.ordering_history&&setOrderingData(res.data.ordering_history);
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const data = React.useMemo(
    () => [
      {
        time: 'Hello',
        action: 'World',
        price: '$1000',
      },
      {
        time: 'React',
        action: 'Table',
        price: '$2000',
      },
      {
        time: 'This',
        action: 'Is a row',
        price: '$3000',
      },
    ],
    []
  )

  const columns = React.useMemo(
    () => [
      {
        Header: 'UTC time',
        accessor: 'time', // accessor is the "key" in the data
      },
      {
        Header: 'Action',
        accessor: 'action',
      },
      {
        Header: 'Price',
        accessor: 'price',
      },
    ],
    []
  );


  return (
    <div>
      <Chart historicaldata={historicaldata} />
      <MyTable columns={columns} data={orderingdata} />
    </div>
    // <>
    //   <div>
    //     <a href="https://vitejs.dev" target="_blank">
    //       <img src={viteLogo} className="logo" alt="Vite logo" />
    //     </a>
    //     <a href="https://react.dev" target="_blank">
    //       <img src={reactLogo} className="logo react" alt="React logo" />
    //     </a>
    //   </div>
    //   <h1>Vite + React</h1>
    //   <div className="card">
    //     <button onClick={() => setCount((count) => count + 1)}>
    //       count is {count}
    //     </button>
    //     <p>
    //       Edit <code>src/App.jsx</code> and save to test HMR
    //     </p>
    //   </div>
    //   <p className="read-the-docs">
    //     Click on the Vite and React logos to learn more
    //   </p>
    // </>
  )
}

export default App
