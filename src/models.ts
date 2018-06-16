//
// configurations
//

export enum ConfigParameterType {
    Selection,
    Float,
    Int
}

export interface AvailableConfigParameter {
    type: ConfigParameterType,

    /**
     * If type == ConfigParameterType.Selection -> String[]; otherwise -> {number,number}
     */
    valueRange: String[] | { from: number, to: number }
}

export interface AvailableConfiguration {
    server: string;
    testCollection: string;
    parameters: { [s: string]: AvailableConfigParameter; }
}

export interface SelectedConfigParameter {
    type: ConfigParameterType,
    value: String | number
}

export interface SelectedConfiguration {
    id: number;
    basedOn:AvailableConfiguration;
    parameters: { [s: string]: SelectedConfigParameter; }
}

//
// retrieval results
//

export interface SearchResult {
    basedOn:SelectedConfiguration;
    preprocessingInfo:any;
    results:ResultItem[];
    totalFound:number
}

export interface ResultItem {
    id:string;
    title:string;
    contents:string;

    score:number;
    explanation:string;
}

