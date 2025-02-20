// function to change the order of a table on a specific page 
function load_new_order(strSubURL, objOrderBy) {
   var strLoadURL = "/";
   // get the selected value
   const selectedOption = objOrderBy.options[objOrderBy.selectedIndex];
   const strVal = selectedOption.value;
   // proceed with change if a value exists
   if (strVal.length > 2 && strSubURL.length > 0) {
      strLoadURL = (strSubURL + strVal + "/dsc");
   }
   // go to where the string is pointed to
   window.location.href = strLoadURL;
}