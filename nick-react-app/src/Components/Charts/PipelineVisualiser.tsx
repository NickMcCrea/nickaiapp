import React, { useState, useEffect } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  Node,
  Edge
} from 'react-flow-renderer';

export interface PipelineStep {
  id: string;
  action: string;
  params: any; // Adjust as per your actual param structure
}

interface PipelineVisualiserProps {
  pipelineDefinition: PipelineStep[];
}

const PipelineVisualiser: React.FC<PipelineVisualiserProps> = ({ pipelineDefinition }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  

  useEffect(() => {

    

    console.log('pipelineDefinition', pipelineDefinition);

    const convertToFlowElements = (pipeline: PipelineStep[]): void => {

      console.log('convertToFlowElements input:', pipeline);

      const newNodes: Node[] = pipeline.map((step, index) => ({
        id: step.id,
        type: 'default', // You can define custom node types if needed
        data: { 
          label: (
            <>
              <strong>Action:</strong> {step.action}
              <br />
              <strong>Params:</strong> {JSON.stringify(step.params, null, 2)}
            </>
          )
        },
        position: { x: 100, y: index * 100 }
      }));

      const newEdges: Edge[] = newNodes.slice(1).map((node, i) => ({
        id: `e${newNodes[i].id}-${node.id}`,
        source: newNodes[i].id,
        target: node.id,
        animated: true,
        style: { stroke: '#ddd' },
        arrowHeadType: 'arrow' as const // Using string literal for arrow head type
      }));

      setNodes(newNodes);
      setEdges(newEdges);
    };

    convertToFlowElements(pipelineDefinition);
  }, [pipelineDefinition, setNodes, setEdges]);

  return (
    <div style={{ height: 900 }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
      >
       
        <Background color="#aaa" gap={16} />
      </ReactFlow>
    </div>
  );
};

export default PipelineVisualiser;
