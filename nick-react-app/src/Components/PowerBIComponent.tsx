import React from 'react';
import { PowerBIEmbed } from 'powerbi-client-react';
import { models, IEmbedConfiguration, service } from 'powerbi-client';
import './PowerBIComponent.css';


interface PowerBIReportProps {
    embedUrl: string;
    reportId: string;
    accessToken: string;
}

const PowerBIReport: React.FC<PowerBIReportProps> = ({ embedUrl, reportId, accessToken }) => {
    // Configuration for embedding the report
    const embedConfig: IEmbedConfiguration = {
        type: 'report', // Type of the embed object
        id: reportId, // Report ID
        embedUrl: embedUrl, // Embed URL
        accessToken: accessToken, // Access Token
        tokenType: models.TokenType.Embed, // Token type
        settings: {
            filterPaneEnabled: true,
            navContentPaneEnabled: true,
            
        },
    };

    // Use a generic type for the event parameter
    const eventHandlers = new Map<string, (event?: any) => void>([
        ['loaded', () => console.log('Report loaded')],
        ['rendered', () => console.log('Report rendered')],
        ['error', (event) => {
            if (event) {
                console.error(event.detail);
            } else {
                console.error('An unknown error occurred');
            }
        }]
    ]);

    return (
        <div className="powerbi-container" >
            <PowerBIEmbed
                embedConfig={embedConfig}
                eventHandlers={eventHandlers}
                cssClassName={'powerbi-frame'}
               
            />
        </div>
    );

};

export default PowerBIReport;
