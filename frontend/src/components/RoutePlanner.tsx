import { createSignal, Show } from "solid-js";

type RoutePlannerProps = {
    onAdd: (location: string, date: string) => void;
    route: { location: string; date: string }[];
    onRemove: (index: number) => void;
    loading: boolean;
};

const RoutePlanner = (props: RoutePlannerProps) => {
    const [dateError, setDateError] = createSignal<string | null>(null);

    const handleAdd = (e: Event) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const location = (form.elements.namedItem("location") as HTMLInputElement).value;
        const dateInput = (form.elements.namedItem("date") as HTMLInputElement).value;

        setDateError(null);
        props.onAdd(location, dateInput);
        form.reset();
    };

    return (
        <div style={{ padding: "1cm" }}>
            <h1>Route Planner</h1>
            <form onSubmit={handleAdd} style={{ "margin-bottom": "2rem" }}>
                <input
                    type="text"
                    name="location"
                    placeholder="Enter city"
                    required
                    style={{ "margin-right": "1rem" }}
                />
                <input
                    type="date"
                    name="date"
                    placeholder="dd.mm.yyyy"
                    required
                    style={{ "margin-right": "1rem" }}
                />
                <button type="submit" disabled={props.loading}>
                    {props.loading ? "Adding..." : "Add Point"}
                </button>
                {dateError() && (
                    <p style={{ color: "red", "margin-top": "0.5rem" }}>{dateError()}</p>
                )}
            </form>

            <Show when={props.loading}>
                <p>Loading weather data...</p>
            </Show>

            <h2>Your Route</h2>
            {props.route.length === 0 ? (
                <p>No route points</p>
            ) : (
                <ul>
                    {props.route.map(({ location, date }, index) => (
                        <li key={`${location}-${date}-${index}`} style={{ "margin-bottom": "1rem" }}>
                            {location} on {date.split("-").reverse().join(".")}
                            <button
                                onClick={() => props.onRemove(index)}
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

