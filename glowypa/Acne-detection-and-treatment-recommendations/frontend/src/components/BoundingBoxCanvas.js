import React, { useRef, useEffect } from 'react';

const BoundingBoxCanvas = ({ selectedOptionModeUsed, base64Image, boxes, labelColors, sliderConfidence, overlapThreshold }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!base64Image) return;

    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    const image = new Image();

    // Set the source of the image to the base64 string
    image.src = base64Image;

    const calculateIoU = (boxA, boxB) => {
      const xA = Math.max(boxA.x_min, boxB.x_min);
      const yA = Math.max(boxA.y_min, boxB.y_min);
      const xB = Math.min(boxA.x_max, boxB.x_max);
      const yB = Math.min(boxA.y_max, boxB.y_max);

      const intersectionArea = Math.max(0, xB - xA) * Math.max(0, yB - yA);
      const boxAArea = (boxA.x_max - boxA.x_min) * (boxA.y_max - boxA.y_min);
      const boxBArea = (boxB.x_max - boxB.x_min) * (boxB.y_max - boxB.y_min);

      return intersectionArea / (boxAArea + boxBArea - intersectionArea);
    };

    const filterBoxes = (boxes) => {
      const normalizedThreshold = overlapThreshold / 100;
      const filtered = [];

      boxes.forEach((box, index) => {
        let keep = true;

        for (let otherIndex = 0; otherIndex < boxes.length; otherIndex++) {
          if (index === otherIndex) continue;

          const otherBox = boxes[otherIndex];
          const iou = calculateIoU(box, otherBox);

          if (overlapThreshold === 0 && iou > 0) {
            keep = false;
            break;
          }

          if (iou >= normalizedThreshold) {
            if (box.confidence < otherBox.confidence) {
              keep = false;
              break;
            }
          }
        }

        if (keep && box.confidence + 0.01 >= Number((sliderConfidence / 100).toFixed(2))) {
          filtered.push(box);
        }
      });

      return filtered;
    };

    image.onload = () => {
      canvas.width = image.width;
      canvas.height = image.height;
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.drawImage(image, 0, 0, canvas.width, canvas.height);

      const filteredBoxes = filterBoxes(boxes);

      filteredBoxes.forEach(box => {
        const { x_min, y_min, x_max, y_max, class_name, confidence } = box;
        const width = x_max - x_min;
        const height = y_max - y_min;

        if (labelColors[class_name]) {
          context.fillStyle = labelColors[class_name];
          context.strokeStyle = labelColors[class_name];
        }

        context.globalAlpha = 0.2;
        context.fillRect(x_min, y_min, width, height);
        context.globalAlpha = 1.0;

        context.lineWidth = 1;
        context.strokeRect(x_min, y_min, width, height);

        let label = '';
        if (selectedOptionModeUsed === "all" || selectedOptionModeUsed === "drawall") {
          console.log("selectedOptionModeUsed", selectedOptionModeUsed)
          label = `${class_name} ${Math.round(confidence * 100)}%`;
        } else if (selectedOptionModeUsed === "drawlabel") {
          label = `${class_name}`;
        } else if (selectedOptionModeUsed === "drawconfidence") {
          label = `${Math.round(confidence * 100)}%`;
        }

        context.font = '200 12px Inter, sans-serif';
        context.textAlign = 'left';
        context.textBaseline = 'top';

        const textWidth = context.measureText(label).width;
        const textHeight = 15;
        const padding = 4;

        let backgroundX = x_min;
        let backgroundY = y_min - textHeight - padding * 2;

        if (backgroundX + textWidth + padding * 2 > canvas.width) {
          backgroundX = canvas.width - textWidth - padding * 2;
        }
        if (backgroundY < 0) {
          backgroundY = y_min + padding * 2;
        }

        context.fillStyle = labelColors[class_name];
        context.fillRect(backgroundX, backgroundY, textWidth + padding * 2, textHeight + padding * 2);

        context.fillStyle = 'black';
        context.fillText(label, backgroundX + padding, backgroundY + padding);
      });
    };

    image.onerror = () => {
      console.error('Failed to load image');
    };
  }, [base64Image, boxes, labelColors, sliderConfidence, overlapThreshold, selectedOptionModeUsed]);

  return <canvas ref={canvasRef} />;
};

export default BoundingBoxCanvas;
