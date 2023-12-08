import { DataSourceMetaDeta } from './DataSourceMetaDeta';
import  ChatService  from '../Services/ChatService';

// Define a type for the DataSourceCatalogueDisplay props
export type DataSourceCatalogueDisplayProps = {
  dataSources: DataSourceMetaDeta[];
  commentary: string;
  onPowerBiClick: (powerBiValue: string) => void;
  chatService: ChatService
};
