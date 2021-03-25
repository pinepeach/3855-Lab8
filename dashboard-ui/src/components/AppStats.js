import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://architect.eastus2.cloudapp.azure.com:8100/stat`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>sales</th>
							<th>returns</th>
						</tr>
						<tr>
							<td># return_product: {stats['return_product']}</td>
							<td># sale_product: {stats['sale_product']}</td>
						</tr>
						<tr>
							<td colspan="2">gcid: {stats['gcid']}</td>
						</tr>
						<tr>
							<td colspan="2">title: {stats['title']}</td>
						</tr>
					</tbody>
                </table>
                <h3>timestamp: {stats['timestamp']}</h3>

            </div>
        )
    }
}
