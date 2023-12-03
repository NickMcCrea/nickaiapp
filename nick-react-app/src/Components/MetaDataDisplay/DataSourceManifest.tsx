import { Field } from './DataSet';

export interface DataSourceManifest {
  name: string;
  description: string;
  displayname?: string;
  version?: string;
  owner?: string;
  category?: string;
  powerbi?: string;
  fields: Field[];
}
