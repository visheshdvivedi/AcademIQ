import { useEffect } from "react";
import { useLocation } from "react-router-dom";

import "preline/preline";
import { IStaticMethods } from "preline/preline";

declare global {
    interface Window {
        HSStaticMethods: IStaticMethods;
    }
}

function App() {
    const location = useLocation();

    useEffect(() => {
        window.HSStaticMethods.autoInit();
    }, [location.pathname]);

    return (
        <>
            <h1 className='font-bold text-2xl'>Hello World</h1>
        </>
    )
}

export default App