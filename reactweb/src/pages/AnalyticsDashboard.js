import React, { useState, useEffect } from "react";
import axios from "axios";
import {
    FunnelChart, Funnel, Tooltip, LabelList,
    LineChart, Line, XAxis, YAxis, CartesianGrid, Legend
} from "recharts";

const API_BASE = "http://localhost:8000";

const AnalyticsDashboard = () => {
    const [events, setEvents] = useState([]);
    const [analytics, setAnalytics] = useState(null);
    const [topProducts, setTopProducts] = useState([]);
    const [timeseries, setTimeseries] = useState([]);
    const [recent, setRecent] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    const [filterType, setFilterType] = useState("all");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    useEffect(() => {
        const load = async () => {
            setIsLoading(true);
            try {
                const ev = await axios.get(`${API_BASE}/analytics/events`);
                const summary = await axios.get(`${API_BASE}/analytics/summary`);
                const top = await axios.get(`${API_BASE}/analytics/top`);
                const ts = await axios.get(`${API_BASE}/analytics/timeseries`);
                const rc = await axios.get(`${API_BASE}/analytics/recent`);

                setEvents(ev.data.events);
                setAnalytics(summary.data);
                setTopProducts(top.data);
                setTimeseries(ts.data);
                setRecent(rc.data);

            } catch (err) {
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };
        load();
    }, []);

    const filteredEvents = events.filter(e => {
        const match = filterType === "all" || e.event_type === filterType;
        const date = new Date(e.timestamp);
        const inRange =
            (!startDate || date >= new Date(startDate)) &&
            (!endDate || date <= new Date(endDate));
        return match && inRange;
    });

    if (isLoading) return <div>Loading analytics...</div>;

    return (
        <div style={{ padding: 20 }}>
            <h1>Analytics Dashboard</h1>

            {/* Filters */}
            <div>
                <select value={filterType} onChange={e => setFilterType(e.target.value)}>
                    <option value="all">All</option>
                    <option value="product_view">Product View</option>
                    <option value="add_to_cart">Add to Cart</option>
                    <option value="purchase">Purchase</option>
                </select>

                <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
                <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
            </div>

            {/* Summary */}
            <h3>Total Events: {analytics.total_events}</h3>

            {/* Funnel */}
            <FunnelChart width={400} height={300}>
                <Tooltip />
                <Funnel dataKey="value" data={[
                    { stage: "Viewed", value: analytics.event_counts.product_view || 0 },
                    { stage: "Cart", value: analytics.event_counts.add_to_cart || 0 },
                    { stage: "Purchase", value: analytics.event_counts.purchase || 0 }
                ]}>
                    <LabelList position="right" dataKey="stage" />
                </Funnel>
            </FunnelChart>

            {/* Timeseries */}
            <h3>Views Over Time</h3>
            <LineChart width={650} height={300} data={timeseries}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="count" stroke="#8884d8" />
            </LineChart>

            {/* Top Products */}
            <h3>Top Viewed Products</h3>
            <ul>
                {topProducts.map(p => (
                    <li key={p.product_id}>Product {p.product_id}: {p.count} views</li>
                ))}
            </ul>

            {/* Recent */}
            <h3>Recent Events</h3>
            <ul>
                {recent.map(e => (
                    <li key={e.timestamp}>
                        <strong>{e.event_type}</strong> | Product {e.product_id} | User {e.user_id}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AnalyticsDashboard;
