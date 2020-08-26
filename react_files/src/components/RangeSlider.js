import React from "react";
import { Slider } from "@material-ui/core";

const RangeSlider = (props) => {
  const [value, setValue] = React.useState([props.minValue, props.maxValue]);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  const rangeStep = props.type === "year" ? 1 : 0.1;

  const marks = [
    { value: props.minValue, label: props.minValue },
    { value: props.maxValue, label: props.maxValue },
  ];
  return (
    <div>
      <Slider
        id={props.id}
        value={value}
        min={props.minValue}
        max={props.maxValue}
        marks={marks}
        step={rangeStep}
        onChange={handleChange}
        valueLabelDisplay="auto"
        aria-labelledby="range-slider"
        onChangeCommitted={props.handler}
      />
    </div>
  );
};
export default RangeSlider;
