document.addEventListener(
    "DOMContentLoaded",
    function(){


        const canvas =
        document.getElementById(
            "transactionChart"
        );


        if(!canvas)
        {
            console.log(
                "Chart canvas tidak ditemukan"
            );

            return;
        }



        new Chart(
            canvas,
            {

            type:"bar",


            data:{


                labels:[

                    "Total",
                    "Pending",
                    "Success",
                    "Failed"

                ],



                datasets:[{


                    label:
                    "Transaksi",



                data:[

                    parseInt(
                        canvas.dataset.total,
                        10
                    ) || 0,

                    parseInt(
                        canvas.dataset.pending,
                        10
                    ) || 0,

                    parseInt(
                        canvas.dataset.success,
                        10
                    ) || 0,

                    parseInt(
                        canvas.dataset.failed,
                        10
                    ) || 0


                ]


                }]


            },


            options:{


                responsive:true,


                maintainAspectRatio:false


            }


            }

        );


    }
);