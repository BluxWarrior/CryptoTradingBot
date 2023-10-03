import React, { useState } from "react";
import axios from "axios";
import './App.css'
import Chart from './componenets/chart'
import MyTable from './componenets/table'

function App() {
  const [historicaldata, setHistoricalData] = useState([]);

  

  React.useEffect(() => {
    const interval = setInterval(() => {
      axios
        .get("http://localhost:5000/api/fetchdata")
        .then((res) => {
          console.log(res);
          console.log(res.data);
          setHistoricalData(res.data);
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // const historicaldata = React.useMemo(
  //   () => [
  //     { time: 'A', price: 400, MA50: 240, MA200: 100 },
  //     { time: 'B', price: 600, MA50: 480, MA200: 480 },
  //     { time: 'C', price: 800, MA50: 360, MA200: 240 },
  //     { time: 'D', price: 1000, MA50: 800, MA200: 990 },
  //     { time: 'E', price: 1200, MA50: 540, MA200: 760 },
  //     { time: 'F', price: 1400, MA50: 960, MA200: 640 },
  //     { time: 'G', price: 1600, MA50: 780, MA200: 840 },
  //     { time: 'H', price: 1800, MA50: 620, MA200: 680 },
  //   ],
  //   []
  // )

  const data = React.useMemo(
    () => [
      {
        time: 'Hello',
        ordertype: 'World',
        price: '$1000',
      },
      {
        time: 'React',
        ordertype: 'Table',
        price: '$2000',
      },
      {
        time: 'This',
        ordertype: 'Is a row',
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
        Header: 'Order Type',
        accessor: 'ordertype',
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
      {/* <Chart historicaldata={historicaldata} /> */}
      <MyTable columns={columns} data={data} />
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
