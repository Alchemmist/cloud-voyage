import { createSignal } from "solid-js";

type RoutePlannerProps = {
    onAdd: (location: string, date: string) => void;
    route: { location: string; date: string }[];
    onRemove: (location: string, date: string) => void;
};

const RoutePlanner = (props: RoutePlannerProps) => {
    const handleAdd = (e: Event) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const location = (
            form.elements.namedItem("location") as HTMLInputElement
        ).value;
        const date = (form.elements.namedItem("date") as HTMLInputElement)
            .value;
        props.onAdd(location, date);
        form.reset();
    };

    return (
        <div style={{ padding: "1cm" }}>
            <h1>Route Planner</h1>
            <form onSubmit={handleAdd} style={{ "margin-bottom": "2rem" }}>
                <input
                    type="text"
                    name="location"
                    placeholder="Enter a city"
                    required
                    style={{ "margin-right": "1rem" }}
                />
                <input
                    type="date"
                    name="date"
                    required
                    style={{ "margin-right": "1rem" }}
                />
                <button type="submit">Add Point</button>
            </form>
            <h2>Selected Route</h2>
            {props.route.length === 0 ? (
                <p>No points selected</p>
            ) : (
                <ul>
                    {props.route.map(({ location, date }) => (
                        <li
                            key={`${location}-${date}`}
                            style={{ "margin-bottom": "1rem" }}
                        >
                            {location} on {date}
                            <button
                                onClick={() => props.onRemove(location, date)}
                                style={{ "margin-left": "1rem" }}
                            >
                                Remove
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default RoutePlanner;
